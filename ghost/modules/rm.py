# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys

from ghost.ghostlib.GhostModule import config, GhostModule, GhostArgumentParser
from ghost.ghostlib.GhostCompleter import remote_path_completer

if sys.version_info.major > 2:
    basestring = str

__class_name__ = 'rm'


@config(cat="admin")
class rm(GhostModule):
    """ remove a file or a directory """

    is_module = False
    dependencies = ['ghostutils.basic_cmds']

    @classmethod
    def init_argparse(cls):
        cls.arg_parser = GhostArgumentParser(prog="rm", description=cls.__doc__)
        cls.arg_parser.add_argument(
            'path', type=str, action='store',
            completer=remote_path_completer
        )

    def run(self, args):
        try:
            rm = self.client.remote('ghostutils.basic_cmds', 'rm', False)

            r = rm(args.path)
            if r:
                self.log(r)
        except Exception as e:
            self.error(
                ' '.join(x for x in e.args if isinstance(x, basestring))
            )
