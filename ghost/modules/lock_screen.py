# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ghost.ghostlib.GhostModule import config, GhostModule, GhostArgumentParser

import subprocess

__class_name__="GhostMod"

@config(compat=["windows", "darwin"], cat="manage", tags=["lock", "screen", "session"])
class GhostMod(GhostModule):
    """ Lock the session """

    @classmethod
    def init_argparse(cls):
        cls.arg_parser = GhostArgumentParser(prog="lock_screen", description=cls.__doc__)

    def run(self, args):
        ok = False
        if self.client.is_windows():
            ok = self.client.conn.modules['ctypes'].windll.user32.LockWorkStation()
        elif self.client.is_darwin():
            ok = self.client.conn.modules.subprocess.Popen(
                '/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession -suspend',
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

        if ok:
            self.success("windows locked")
        else:
            self.error("couldn't lock the screen")
