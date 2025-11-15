# -*- encoding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__all__ = (
    'Proxy', 'getLogger',
    'GhostSocketStream', 'GhostUDPSocketStream',
    'chain_transports',
    'GhostTCPServer', 'GhostUDPServer',
    'GhostTCPClient', 'GhostSSLClient',
    'GhostProxifiedTCPClient', 'GhostProxifiedSSLClient',
    'GhostUDPClient',
    'DummyGhostTransport',

    'RSA_AESClient', 'RSA_AESServer',
    'GhostHTTPClient', 'GhostHTTPServer',
    'GhostWebSocketClient', 'GhostWebSocketServer',
    'EC4TransportServer', 'EC4TransportClient',
    'ECMTransportServer', 'ECMTransportClient'
)

import logging

from collections import namedtuple

Proxy = namedtuple(
    'Proxy', [
       'type', 'addr', 'username', 'password'
    ]
)

logger = logging.getLogger('ghost.network')


def getLogger(name):
    return logger.getChild(name)


from .streams.GhostSocketStream import GhostSocketStream


try:
    from .streams.GhostSocketStream import GhostUDPSocketStream
except:
    GhostUDPSocketStream = None


from .base import chain_transports
from .servers import GhostTCPServer, GhostUDPServer
from .clients import GhostTCPClient, GhostSSLClient
from .clients import GhostProxifiedTCPClient, GhostProxifiedSSLClient
from .clients import GhostUDPClient

from .transports.dummy import DummyGhostTransport


try:
    from .transports.rsa_aes import RSA_AESClient, RSA_AESServer
except Exception as e:
    logger.exception('Transport rsa_aes disabled: %s', e)
    RSA_AESClient = None
    RSA_AESServer = None

try:
    from .transports.http import GhostHTTPClient, GhostHTTPServer
except Exception as e:
    logger.exception('Transport http disabled: %s', e)
    GhostHTTPClient = None
    GhostHTTPServer = None

try:
    from .transports.websocket import GhostWebSocketClient, GhostWebSocketServer
except Exception as e:
    logger.exception('Transport websocket disabled: %s', e)
    GhostWebSocketClient = None
    GhostWebSocketServer = None

try:
    from .transports.ec4 import EC4TransportServer, EC4TransportClient
except Exception as e:
    logger.exception('Transport ec4 disabled: %s', e)
    EC4TransportServer = None
    EC4TransportClient = None

try:
    from .transports.ecm import ECMTransportServer, ECMTransportClient
except Exception as e:
    logger.exception('Transport ecm disabled: %s', e)
    ECMTransportServer = None
    ECMTransportClient = None

