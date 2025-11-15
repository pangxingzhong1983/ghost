# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from ghost.ghostlib.GhostModule import config, GhostModule, GhostArgumentParser

__class_name__="PsModule"

@config(cat="admin")
class PsModule(GhostModule):
    """ list process information """
    is_module=False

    @classmethod
    def init_argparse(cls):
        cls.arg_parser = GhostArgumentParser(prog="getpid", description=cls.__doc__)

    def run(self, args):
        getpid = self.client.remote('os', 'getpid')
        pid = getpid()
        self.success('PID: {}'.format(pid))
