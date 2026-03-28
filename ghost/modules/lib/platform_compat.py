# -*- coding: utf-8 -*-
"""
平台兼容性辅助函数（工程增强）
"""

from __future__ import absolute_import


def detect_platform(client):
    """Return normalized platform tags for current client."""
    tags = set()
    if client is None:
        return tags

    if hasattr(client, 'is_windows') and client.is_windows():
        tags.update(['windows'])
    elif hasattr(client, 'is_linux') and client.is_linux():
        tags.update(['linux', 'posix'])
    elif hasattr(client, 'is_darwin') and client.is_darwin():
        tags.update(['darwin', 'posix'])

    return tags


def is_compatible(module_platforms, current_platforms):
    """Check whether module platform declarations match current platform tags."""
    if not module_platforms:
        return True

    supported_set = set(module_platforms)
    return bool(current_platforms & supported_set)


def build_unsupported_message(module_name, module_platforms, current_platforms):
    """Build readable error message for incompatible module execution."""
    current_str = '/'.join(sorted(current_platforms)) if current_platforms else 'unknown'
    supported = ', '.join(sorted(set(module_platforms))) if module_platforms else 'all'

    return "模块 '{}' 不支持当前平台 '{}'。支持平台：{}。".format(
        module_name, current_str, supported
    )
