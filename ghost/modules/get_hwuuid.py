# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from ghost.ghostlib.GhostModule import config, GhostModule, GhostArgumentParser

__class_name__ = "GetHwUuid"

@config(cat="gather")
class GetHwUuid(GhostModule):
    """ Try to get UUID (DMI) or machine-id (dbus/linux) """
    dependencies = {
        'windows': ['win32api', 'win32com', 'pythoncom', 'winerror'],
        'all': ['hwuuid']
    }

    @classmethod
    def init_argparse(cls):
        cls.arg_parser = GhostArgumentParser(
            prog='get_hwuuid',
            description=cls.__doc__
        )

    def run(self, args):
        get_hw_uuid = self.client.remote('hwuuid', 'get_hw_uuid')

        method, uuid = get_hw_uuid()
        self.success('{} ({})'.format(method, uuid))
