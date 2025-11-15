# -*- coding: utf-8 -*-
# Copyright (c) 2015, Nicolas VERDIER (contact@n1nj4.eu)
# Ghost is under the BSD 3-Clause license. see the LICENSE file at the root of the project for the detailed licence terms

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from ghost.network.lib import GhostUDPServer, GhostUDPClient, GhostUDPSocketStream
from ghost.network.lib import DummyGhostTransport
from ghost.network.transports import Transport

class TransportConf(Transport):
    info = "Simple UDP transport transmitting in cleartext"
    name="udp_cleartext"
    server=GhostUDPServer
    client=GhostUDPClient
    stream=GhostUDPSocketStream
    client_transport=DummyGhostTransport
    server_transport=DummyGhostTransport
    dgram=True
