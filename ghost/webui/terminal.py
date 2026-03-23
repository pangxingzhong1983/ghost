# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import pty
import fcntl
import signal
import subprocess
import re

import tornado.ioloop
import tornado.websocket

from . import auth
from ghost.ghostlib.utils.term import ESC_REGEX, DEFAULT_MULTIBYTE_CP


class TerminalWebSocket(tornado.websocket.WebSocketHandler):
    def initialize(self, data_dir=None):
        self.data_dir = data_dir
        self._pty_fd = None
        self._proc = None
        self._ansi_tail = b""

    def check_origin(self, origin):
        return True

    def open(self):
        token = self.get_argument("token", "")
        session = auth.get_session(token)
        if not session or not session["is_active"]:
            self.close()
            return
        self._start_shell()

    def on_message(self, message):
        if not self._pty_fd:
            return
        if isinstance(message, str):
            data = message.encode("utf-8", "ignore")
        else:
            data = message
        os.write(self._pty_fd, data)

    def on_close(self):
        self._stop_shell()

    def _start_shell(self):
        master_fd, slave_fd = pty.openpty()
        flags = fcntl.fcntl(master_fd, fcntl.F_GETFL)
        fcntl.fcntl(master_fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
        env = os.environ.copy()
        env.setdefault("TERM", "xterm-256color")
        env.setdefault("HOME", self.data_dir or "/data")
        cmd = [os.environ.get("PYTHON", "python"), "-m", "ghost.cli.ghostsh"]
        if os.environ.get("GHOST_UI_GHOSTSH_ENCRYPT", "0") != "1":
            cmd.append("--not-encrypt")
        self._proc = subprocess.Popen(
            cmd,
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            close_fds=True,
            env=env,
        )
        os.close(slave_fd)
        self._pty_fd = master_fd
        tornado.ioloop.IOLoop.current().add_handler(
            self._pty_fd, self._read_pty, tornado.ioloop.IOLoop.READ
        )

    def _read_pty(self, fd, events):
        try:
            data = os.read(fd, 4096)
        except OSError:
            data = b""
        if not data:
            self._stop_shell()
            return
        try:
            data = (self._ansi_tail or b"") + data
            self._ansi_tail = b""
            partial = re.search(br"\x1b(?:\[[0-?]*[ -/]*)?$", data)
            if partial:
                self._ansi_tail = partial.group(0)
                data = data[:partial.start()]
            data = ESC_REGEX.sub(b"", data)
            data = data.replace(b"\x01", b"").replace(b"\x02", b"")
            text = data.decode(DEFAULT_MULTIBYTE_CP, "ignore")
            text = text.replace("\r\n", "\n").replace("\r", "\n")
            self.write_message(text)
        except Exception:
            self._stop_shell()

    def _stop_shell(self):
        if self._pty_fd:
            try:
                tornado.ioloop.IOLoop.current().remove_handler(self._pty_fd)
            except Exception:
                pass
            try:
                os.close(self._pty_fd)
            except Exception:
                pass
            self._pty_fd = None
        if self._proc:
            try:
                self._proc.send_signal(signal.SIGTERM)
            except Exception:
                pass
            self._proc = None
