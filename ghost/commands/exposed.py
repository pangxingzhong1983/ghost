# -*- encoding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from ghost.ghostlib.GhostModule import GhostArgumentParser
from ghost.ghostlib.GhostOutput import Table

usage = 'list exposed objects/methods'
parser = GhostArgumentParser(description=usage)


def do(server, handler, config, modargs):
    for client in server.get_clients(handler.default_filter):
        objects = []
        with client.conn._conn._local_objects._lock:
            for klass, refcnt in \
              client.conn._conn._local_objects._dict.values():
                objects.append({
                    'OID': id(klass),
                    'Object': repr(klass),
                    'Refs': refcnt
                })

        handler.display(Table(
            objects,
            headers=['OID', 'Object', 'Refs'],
            caption=client.short_name()
        ))
