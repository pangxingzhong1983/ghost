# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
__all__ = [
    'GhostSocketStream',
]

from .GhostSocketStream import GhostSocketStream

try:
    from .GhostSocketStream import GhostUDPSocketStream
    __all__.append('GhostUDPSocketStream')

except ImportError:
    GhostUDPSocketStream = None
