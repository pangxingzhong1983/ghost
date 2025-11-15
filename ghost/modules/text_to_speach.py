# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from ghost.ghostlib.GhostModule import config, GhostModule, GhostArgumentParser

__class_name__="AndroidTTS"

@config(compat="android", cat="troll", tags=["speech", "speak", "sound"])
class AndroidTTS(GhostModule):
    """ Use Android text to speach to say something :) """

    dependencies=['ghostdroid.text_to_speech']

    @classmethod
    def init_argparse(cls):
        cls.arg_parser = GhostArgumentParser(prog="tts", description=cls.__doc__)
        cls.arg_parser.add_argument('--lang', default='US', help='change the locale')
        cls.arg_parser.add_argument('text', help='text to speak out loud')

    def run(self, args):
        self.client.conn.modules['ghostdroid.text_to_speech'].speak(args.text, lang=args.lang)
        self.success("The truth has been spoken !")
