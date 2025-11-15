# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from ghost.ghostlib.GhostModule import config, GhostModule, GhostArgumentParser
from ghost.ghostlib.GhostCompleter import package_completer

__class_name__ = "LoadPackageModule"


@config(cat="manage", compat="all")
class LoadPackageModule(GhostModule):
    """
    Load a python package onto a remote client. Packages files must be placed in one of the ghost/packages/<os>/<arch>/ repository
    """

    @classmethod
    def init_argparse(cls):
        cls.arg_parser = GhostArgumentParser(prog="load_package", description=cls.__doc__)
        cls.arg_parser.add_argument('-f', '--force', action='store_true', help='force package to reload even '
                                                                               'if it has already been loaded')
        cls.arg_parser.add_argument('-r', '--remove', action='store_true', help='remove (invalidate) module')
        cls.arg_parser.add_argument('-d', '--dll', action='store_true', help='load a dll instead')
        cls.arg_parser.add_argument('package', completer=package_completer, help='package name '
                                                                                 '(example: psutil, scapy, ...)')

    def run(self, args):
        if args.dll:
            if self.client.load_dll(args.package):
                self.success('dll loaded')
            else:
                self.error('the dll was already loaded')
        elif args.remove:
            invalidated = self.client.invalidate_packages([args.package])
            if invalidated:
                self.success('package invalidated')
        else:
            if self.client.load_package(args.package, force=args.force):
                self.success('package loaded')
            else:
                self.warning('package is already loaded')
