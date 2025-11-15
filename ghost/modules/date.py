# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
from ghost.ghostlib.GhostModule import config, GhostArgumentParser, GhostModule

if sys.version_info.major > 2:
    basestring = str

__class_name__ = 'date'


@config(cat="admin")
class date(GhostModule):
    """ Get current date """
    is_module=False

    dependencies = ['ghostutils.basic_cmds']

    @classmethod
    def init_argparse(cls):
        cls.arg_parser = GhostArgumentParser(prog="date", description=cls.__doc__)

    def run(self, args):
        try:
            date = self.client.remote('ghostutils.basic_cmds', 'now', False)
            self.success(date())

        except Exception as e:
            self.error(
                ' '.join(x for x in e.args if isinstance(x, basestring))
            )
