# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from ghost.ghostlib.GhostModule import GhostModule, GhostArgumentParser
from ghost.ghostlib.GhostErrors import GhostModuleError

__class_name__="ExitModule"

class ExitModule(GhostModule):
    """ exit the client on the other side """
    is_module=False

    @classmethod
    def init_argparse(cls):
        cls.arg_parser = GhostArgumentParser(prog="exit", description=cls.__doc__)
        cls.arg_parser.add_argument('--yes', action="store_true", help='exit confirmation')

    def run(self, args):
        if args.yes:
            try:
                self.client.conn.exit()
            except Exception:
                pass
        else:
            raise GhostModuleError('Please conform with --yes to perform this action.')
