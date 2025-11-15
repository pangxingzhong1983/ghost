# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from ghost.ghostlib.GhostModule import config, GhostModule, GhostArgumentParser

__class_name__="PsModule"

@config(cat="admin")
class PsModule(GhostModule):
    """ list parent process information """
    is_module=False

    dependencies = {
        'windows': ['pupwinutils.processes']
    }

    @classmethod
    def init_argparse(cls):
        cls.arg_parser = GhostArgumentParser(prog="getppid", description=cls.__doc__)

    def run(self, args):
        if self.client.is_windows():
            get_current_ppid = self.client.remote('pupwinutils.processes', 'get_current_ppid')
            outputlist = get_current_ppid()
            for out in outputlist:
                self.success('%s: %s' % (out, outputlist[out]))
            return # quit
        else:
            getppid = self.client.remote('os', 'getppid')
            self.success('PPID: {}'.format(getppid()))
