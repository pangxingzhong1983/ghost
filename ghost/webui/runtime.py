# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import subprocess
import threading
import sys

# Avoid importing GhostCmdLoop in ghost.ghostlib __init__ to prevent circular imports.
sys.__ghost_main__ = True

from ghost.commands import Commands, InvalidCommand
from ghost.ghostlib.GhostConfig import GhostConfig
from ghost.ghostlib.GhostServer import GhostServer
from ghost.ghostlib.GhostCredentials import Credentials
from ghost.ghostlib.GhostCmd import IOGroup, ObjectStream
from ghost.ghostlib.GhostErrors import GhostModuleExit, GhostModuleError, GhostModuleUsageError
from ghost.ghostlib.GhostModule import REQUIRE_NOTHING, REQUIRE_REPL, REQUIRE_TERMINAL
from ghost.ghostlib.GhostOutput import Error, Line, Color, Success, Warn, Info, ServiceInfo
from ghost.ghostlib.utils.term import as_term_bytes, remove_esc, DEFAULT_MULTIBYTE_CP
from ghost.network.lib.base_launcher import LauncherError


class InteractiveCommandError(Exception):
    pass


class OutputBuffer(object):
    def __init__(self):
        self._lock = threading.Lock()
        self._parts = []

    def write(self, text, nocrlf=False):
        if text is None:
            return
        data = as_term_bytes(text)
        data = remove_esc(data)
        chunk = data.decode(DEFAULT_MULTIBYTE_CP, "ignore")
        if not nocrlf:
            chunk += "\n"
        with self._lock:
            self._parts.append(chunk)

    def getvalue(self):
        with self._lock:
            return "".join(self._parts)


class WebHandler(object):
    def __init__(self, server, config):
        self.server = server
        self.config = config
        self.default_filter = None
        self.display_lock = threading.Lock()
        self._buffer = OutputBuffer()

    def set_buffer(self, buffer):
        self._buffer = buffer or OutputBuffer()

    def display(self, text, nocrlf=False, to_bytes=False):
        with self.display_lock:
            self._buffer.write(text, nocrlf=nocrlf)

    def display_srvinfo(self, msg):
        self.display(Info(msg))

    def display_success(self, msg):
        self.display(Success(msg))

    def display_warning(self, msg):
        self.display(Warn(msg))

    def display_error(self, msg):
        self.display(Error(msg))

    def acquire_io(self, requirements, amount, background=False, pipe=None):
        if requirements in (REQUIRE_REPL, REQUIRE_TERMINAL):
            raise InteractiveCommandError("interactive module requires terminal")

        stream = requirements != REQUIRE_NOTHING
        if amount == 1 and not background:
            return [
                IOGroup(None, ObjectStream(self.display, stream=stream, pipe=pipe))
            ]
        return [
            IOGroup(None, ObjectStream(stream=stream, pipe=pipe))
            for _ in range(amount)
        ]

    def process(self, job, background=False, daemon=False, unique=False):
        if background or daemon:
            if not unique:
                self.server.add_job(job)
            self.display(ServiceInfo("Background job: {}".format(job)))
            return

        job.worker_pool.join(on_interrupt=job.interrupt)
        if job.module.io not in (REQUIRE_REPL, REQUIRE_TERMINAL):
            self.summary(job)

    def summary(self, job):
        need_title = len(job) > 1
        modules = len(job.ghostmodules)
        for idx, instance in enumerate(job.ghostmodules):
            if not instance.stdout:
                continue
            if need_title:
                self.display(str(instance.client))
            for block in instance.stdout.getvalue():
                self.display(block, instance.stdout.is_stream)
            if idx < modules - 1:
                self.display("")


class GhostRuntime(object):
    def __init__(self):
        self.config = GhostConfig()
        self.credentials = Credentials()
        self.server = GhostServer(self.config, self.credentials)
        self.handler = WebHandler(self.server, self.config)
        self.server.register_handler(self.handler)
        self.commands = Commands()

    def _check_interactive(self, cmdline):
        if not cmdline:
            return None
        aliases = dict(self.config.items("aliases"))
        modules = list(self.server.iter_modules(by_clients=False))
        try:
            command, args = self.commands._get_command(cmdline, aliases, modules, True)
        except InvalidCommand:
            return None

        if command == self.commands.get("python"):
            return "python"

        if command == self.commands.get("run"):
            parser = command.parser
            if callable(parser):
                parser = parser(self.server, self.handler, self.config)
            try:
                modargs = parser.parse_args(args)
            except GhostModuleUsageError:
                return None
            module = self.server.get_module(
                self.server.get_module_name_from_category(modargs.module)
            )
            if module and module.io in (REQUIRE_REPL, REQUIRE_TERMINAL):
                return module.get_name()
        return None

    def run_command(self, cmdline, allow_shell=False):
        buffer = OutputBuffer()
        self.handler.set_buffer(buffer)

        if cmdline.startswith("!"):
            if not allow_shell:
                return buffer.getvalue(), "shell command not allowed"
            return self._run_shell(cmdline[1:].strip())

        interactive = self._check_interactive(cmdline)
        if interactive:
            return buffer.getvalue(), "interactive command requires terminal"

        try:
            self.commands.execute(
                self.server, self.handler, self.config, cmdline
            )
        except GhostModuleUsageError as e:
            prog, message, usage = e.args
            self.handler.display(Line(Error(message, prog)))
            self.handler.display(usage)
        except GhostModuleExit:
            pass
        except InvalidCommand as e:
            self.handler.display(Error(
                "Unknown (or unavailable) command {}. Use help -M to list available commands and modules".format(e)
            ))
        except (GhostModuleError, LauncherError, NotImplementedError, ValueError) as e:
            if str(e) and str(e) != "None":
                self.handler.display(Error(e))

        return buffer.getvalue(), None

    def _run_shell(self, command):
        proc = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=os.environ.copy(),
        )
        out, _ = proc.communicate()
        if out is None:
            out = b""
        if not isinstance(out, bytes):
            out = out.encode("utf-8")
        text = out.decode("utf-8", "ignore")
        if proc.returncode != 0:
            return text, "command failed with code {}".format(proc.returncode)
        return text, None
