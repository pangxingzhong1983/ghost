# -*- coding: utf-8 -*-
# Copyright (c) 2015, Nicolas VERDIER (contact@n1nj4.eu)
# Ghost is under the BSD 3-Clause license. see the LICENSE file at the root of the project for the detailed licence terms

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from io import open

from ghost.ghostlib.GhostModule import (
    config, GhostModule, GhostArgumentParser,
    REQUIRE_STREAM
)

from ghost.ghostlib.GhostErrors import GhostModuleError
from ghost.ghostlib.GhostCompleter import path_completer
from ghost.ghostlib.utils.rpyc_utils import redirected_stdio

__class_name__="PythonExec"


@config(cat="admin")
class PythonExec(GhostModule):
    """ execute python code on a remote system """

    io = REQUIRE_STREAM

    @classmethod
    def init_argparse(cls):
        cls.arg_parser = GhostArgumentParser(prog='pyexec', description=cls.__doc__)
        cls.arg_parser.add_argument('--file', metavar="<path>", completer=path_completer, help="execute code from .py file")
        cls.arg_parser.add_argument('-R', '--no-redirected-stdio', action='store_true', default=False, help="Do not redirect stdio (no output)")
        cls.arg_parser.add_argument('-c','--code', metavar='<code string>', help="execute python oneliner code. ex : 'import platform;print platform.uname()'")

    def run(self, args):
        code=""
        if args.file:
            self.info("loading code from %s ..."%args.file)
            with open(args.file,'r') as f:
                code = f.read()
        elif args.code:
            code = args.code
        else:
            raise GhostModuleError("--code or --file argument is mandatory")

        if args.no_redirected_stdio:
            self.client.conn.execute(code+"\n")
        else:
            with redirected_stdio(self):
                self.client.conn.execute(code+"\n")
