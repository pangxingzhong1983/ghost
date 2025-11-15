# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from ghost.network.transports import Transport, LAUNCHER_TYPE_BIND
from ghost.network.lib import GhostTCPServer, GhostTCPClient, GhostSocketStream
from ghost.network.lib import ECMTransportClient, ECMTransportServer

class TransportConf(Transport):
    info = "ECPV + AES/GCM"
    name = "ecm"
    server = GhostTCPServer
    client = GhostTCPClient
    stream = GhostSocketStream
    client_transport = ECMTransportClient
    server_transport = ECMTransportServer

    # Reuse EC4 creds
    credentials = ['ECPV_RC4_PUBLIC_KEY', 'ECPV_RC4_PRIVATE_KEY']

    def __init__(self, *args, **kwargs):
        Transport.__init__(self, *args, **kwargs)
        try:
            import ghost_credentials
            PUB_KEY = ghost_credentials.ECPV_RC4_PUBLIC_KEY
            PRIV_KEY = ghost_credentials.ECPV_RC4_PRIVATE_KEY

        except ImportError:
            from ghost.ghostlib.GhostCredentials import Credentials
            credentials = Credentials()
            PUB_KEY = credentials['ECPV_RC4_PUBLIC_KEY']
            PRIV_KEY = credentials['ECPV_RC4_PRIVATE_KEY']

        if self.launcher_type == LAUNCHER_TYPE_BIND:
            self.client_transport = ECMTransportServer.custom(privkey=PRIV_KEY)
            self.server_transport = ECMTransportClient.custom(pubkey=PUB_KEY)

        else:
            self.server_transport = ECMTransportServer.custom(privkey=PRIV_KEY)
            self.client_transport = ECMTransportClient.custom(pubkey=PUB_KEY)
