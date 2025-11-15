# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys

from ghost.ghostlib.GhostModule import config, GhostModule, GhostArgumentParser
from ghost.ghostlib.GhostCompleter import remote_path_completer, remote_dirs_completer

__class_name__ = 'mv'

if sys.version_info.major > 2:
    basestring = str


@config(cat="admin")
class mv(GhostModule):
    """ move file or directory """
    is_module = False

    dependencies = ['ghostutils.basic_cmds']

    @classmethod
    def init_argparse(cls):
        cls.arg_parser = GhostArgumentParser(prog="mv", description=cls.__doc__)
        cls.arg_parser.add_argument('src', type=str, action='store', completer=remote_path_completer)
        cls.arg_parser.add_argument('dst', type=str, action='store', completer=remote_dirs_completer)

    def run(self, args):
        try:
            mv = self.client.remote('ghostutils.basic_cmds', 'mv')

            r = mv(args.src, args.dst)
            if r:
                self.log(r)

        except Exception as e:
            self.error(
                ' '.join(x for x in e.args if isinstance(x, basestring))
            )

