# -*- coding: utf-8 -*-

__all__ = ('apply_dl_hacks',)

import os
import sys
if not "rustc" in sys.version:
    import ctypes
else:
    ctypes=None
import ghost.agent as ghost

try:
    import ctypes.util
    have_ctypes_util = True
except ImportError:
    have_ctypes_util = False

have_ctypes_dlopen = hasattr(ctypes, '_dlopen')

NATIVE_LIB_PATTERNS = [
    'lib{}.so', '{}.so',
    'lib{}.pyd', '{}.pyd',
    'lib{}.dll', '{}.dll',
    'lib{}310.dll'
]


def _find_library(name):
    ghost.dprint('_find_library called: {} => {}', name)
    for pattern in NATIVE_LIB_PATTERNS:
        libname = pattern.format(name)
        try:
            return ctypes.CDLL(libname)
        except:
            pass
    ghost.dprint('library {} not found ...', name)


def _ghost_make_library_path(name):
    if not name:
        return

    if 'ghost:' in name:
        name = name[name.find('ghost:')+5:]
        name = os.path.relpath(name)
        name = '/'.join([
            x for x in name.split(os.path.sep) if x and x not in ('.', '..')
        ])

    return name


def _ghost_find_library(name):
    import ghost_modules
    ghostized = _ghost_make_library_path(name)
    if ghostized in ghost_modules.modules:
        ghost.dprint('FIND LIBRARY: {} => {}', name, ghostized)
        return ghostized
    else:
        return ctypes.util._system_find_library(name)


def _ghost_dlopen(name, *args, **kwargs):
    ghost.dprint('ctypes dlopen: {}', name)

    if name and name.startswith("exposed_"):
        ghost.dprint('_ghost_dlopen: RPYC hotpatch : renaming %s to %s'%(name, name[8:]))
        name=name[8:]

    name = _ghost_make_library_path(name)
    ghost.dprint(
        'ctypes dlopen / ghostized: {} (system {})',
        name, ctypes._system_dlopen)

    handle = ghost.load_dll(name)
    if handle:
        ghost.dprint(
            'ctypes dlopen / ghostized : {} found in-memory handle', name)
        return handle
    else:
        ghost.dprint('load_dll by name ({}) failed', name)

    return ctypes._system_dlopen(name, *args, **kwargs)


def apply_dl_hacks():
    if have_ctypes_dlopen:
        setattr(ctypes, '_system_dlopen', ctypes._dlopen)

    if have_ctypes_util:
        ctypes.util._system_find_library = ctypes.util.find_library

        if hasattr(ctypes.util, '_findLib_gcc'):
            ctypes.util._findLib_gcc = lambda name: None
    else:
        ctypes_util = ghost.make_module('ctypes.util')

        setattr(ctypes_util, '_system_find_library', _find_library)

    ctypes._dlopen = _ghost_dlopen
    ctypes.util.find_library = _ghost_find_library

    libpython = None

    if sys.platform == 'win32':
        try:
            libpython = ctypes.PyDLL('python310.dll')
        except WindowsError:
            ghost.dprint('python310.dll not found')
    else:
        for libname in (None, 'python310.so'):
            try:
                candidate = ctypes.PyDLL(libname)
            except OSError:
                continue

            if hasattr(candidate, '_Py_PackageContext'):
                libpython = candidate
                break

    if libpython is not None:
        ghost.dprint('Set ctypes.pythonapi to {}', libpython)
        ctypes.pythonapi = libpython
