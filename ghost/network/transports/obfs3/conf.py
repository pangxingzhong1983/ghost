# -*- coding: utf-8 -*-
# Copyright (c) 2015, Nicolas VERDIER (contact@n1nj4.eu)
# Ghost is under the BSD 3-Clause license. see the LICENSE file at the root of the project for the detailed licence terms

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from ghost.network.transports import Transport, LAUNCHER_TYPE_BIND
from ghost.network.lib import GhostTCPServer, GhostTCPClient, GhostSocketStream
from ghost.network.lib import RSA_AESClient, RSA_AESServer
from ghost.network.lib import chain_transports
from ghost.network.lib.transports.obfs3.obfs3 import Obfs3Client, Obfs3Server

class TransportConf(Transport):
    info = "TCP transport using obfsproxy's obfs3 transport with a extra rsa+aes layer"
    name = "obfs3"
    server = GhostTCPServer
    client = GhostTCPClient
    stream = GhostSocketStream
    credentials = ['SIMPLE_RSA_PUB_KEY', 'SIMPLE_RSA_PRIV_KEY']

    def __init__(self, *args, **kwargs):
        Transport.__init__(self, *args, **kwargs)

        try:
            import ghost_credentials
            RSA_PUB_KEY = ghost_credentials.SIMPLE_RSA_PUB_KEY
            RSA_PRIV_KEY = ghost_credentials.SIMPLE_RSA_PRIV_KEY

        except ImportError:
            from ghost.ghostlib.GhostCredentials import Credentials
            credentials = Credentials()
            RSA_PUB_KEY = credentials['SIMPLE_RSA_PUB_KEY']
            RSA_PRIV_KEY = credentials['SIMPLE_RSA_PRIV_KEY']

        if self.launcher_type == LAUNCHER_TYPE_BIND:
            self.client_transport = chain_transports(
                    Obfs3Client,
                    RSA_AESServer.custom(privkey=RSA_PRIV_KEY, rsa_key_size=4096, aes_size=256),
                )
            self.server_transport = chain_transports(
                    Obfs3Server,
                    RSA_AESClient.custom(pubkey=RSA_PUB_KEY, rsa_key_size=4096, aes_size=256),
                )

        else:
            self.client_transport = chain_transports(
                    Obfs3Client,
                    RSA_AESClient.custom(pubkey=RSA_PUB_KEY, rsa_key_size=4096, aes_size=256),
                )
            self.server_transport = chain_transports(
                    Obfs3Server,
                    RSA_AESServer.custom(privkey=RSA_PRIV_KEY, rsa_key_size=4096, aes_size=256),
                )
