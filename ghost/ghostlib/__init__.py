# -*- coding: utf-8 -*-

__all__ = [
    'getLogger', 'GhostCmdLoop', 'GhostService',
    'GhostConfig', 'GhostServer', 'GhostModule',
    'Credentials', 'GhostClient',
    'ROOT',
    'HOST_SYSTEM', 'HOST_CPU_ARCH', 'HOST_OS_ARCH'
]

import os
import sys
import platform

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
HOST_SYSTEM = platform.system()
HOST_CPU_ARCH = platform.architecture()[0]
HOST_OS_ARCH = platform.machine()


DEPS = [
        os.path.abspath(os.path.join(ROOT, 'library_patches_py3')),
        os.path.abspath(os.path.join(ROOT, 'packages', 'all')),
        ]

for dep in DEPS:
    if not os.path.exists(dep):
        raise Exception("Dependency path not found : {}".format(dep))
    if "library_patches" in dep:
        sys.path.insert(0, dep)
    else:
        sys.path.append(dep)

# dirty, TODO: refactor GhostCompiler to be able to call it standalone
if not getattr(sys, '__from_build_library_zip_compiler__', False):
    from .GhostLogger import getLogger

    from .GhostConfig import GhostConfig
    from .GhostCredentials import Credentials

    from ghost.network.conf import load_network_modules

    load_network_modules()

    if not getattr(sys, '__ghost_main__', False):
        from .GhostCmd import GhostCmdLoop
        from .GhostService import GhostService
        from .GhostModule import GhostModule
        from .GhostClient import GhostClient
        from .GhostServer import GhostServer
