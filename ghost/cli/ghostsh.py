#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------
# Copyright (c) 2015, Nicolas VERDIER (contact@n1nj4.eu)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE
# --------------------------------------------------------------

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import logging
import argparse

# Windows 环境下当前 CLI 不兼容，直接友好退出，避免缺少 termios 导致崩溃
if os.name == 'nt':
    def main():
        print("Ghost shell暂不支持Windows环境（依赖termios等POSIX特性）")
        return 0

    if __name__ == "__main__":
        sys.exit(main())
    else:
        sys.exit(0)

args = None

def parse_args():
    parser = argparse.ArgumentParser(prog='ghostsh', description="Ghost console")
    parser.add_argument(
        '--loglevel', '-d',
        help='change log verbosity', dest='loglevel',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='WARNING')
    parser.add_argument('--logfile', '-DF', help='log to file', dest='logfile', default=None)
    parser.add_argument(
        '-l', '--listen',
        help='Bind server listener with transport and args to port.'
        'Example: -l ssl 127.0.0.1:443 -l kcp 80 -l xyz 1234 OPTION1=value OPTION2=value.',
        nargs='+',
        metavar=('TRANSPORT', '<<EXTERNAL_IP=>IP>:<EXTERNAL_PORT=>PORT OPTION=value'),
        action='append', default=[]
    )
    parser.add_argument(
        '--workdir', help='Set Workdir (Default = current workdir)')
    parser.add_argument('-NE', '--not-encrypt',
                        help='Do not encrypt configuration', action='store_true')
    parser.add_argument('--sound', dest='sounds',
                        help='Play a sound when a session connects', action='store_true')
    return parser

try:
    import ghost.ghostlib.GhostSignalHandler
    assert ghost.ghostlib.GhostSignalHandler
except ImportError:
    pass

from ghost.ghostlib import (
    GhostServer, GhostCmdLoop, GhostCredentials, GhostConfig
)

def main():
    parser = parse_args()
    args = parser.parse_args()
    if args.workdir:
        os.chdir(args.workdir)

        if os.getuid() == 0 and os.getgid() == 0:
            wdstat = os.stat(args.workdir)
            os.setresgid(wdstat.st_uid, wdstat.st_uid, wdstat.st_uid)
            os.setresuid(wdstat.st_uid, wdstat.st_uid, wdstat.st_uid)

    root_logger = logging.getLogger()

    if args.logfile:
        logging_stream = logging.FileHandler(args.logfile)
        logging_stream.setFormatter(
            logging.Formatter(
                '%(asctime)-15s|%(levelname)-5s|%(relativeCreated)6d|%(threadName)s|%(name)s| %(message)s'))
    else:
        logging_stream = logging.StreamHandler()
        logging_stream.setFormatter(logging.Formatter('%(asctime)-15s| %(name)s| %(message)s'))

    logging_stream.setLevel(logging.DEBUG)

    root_logger.handlers = []

    root_logger.addHandler(logging_stream)
    root_logger.setLevel(args.loglevel)
    GhostCredentials.DEFAULT_ROLE = 'CONTROL'
    if args.not_encrypt:
        GhostCredentials.ENCRYPTOR = None

    # Try to initialize credentials before CMD loop
    try:
        credentials = GhostCredentials.Credentials(validate=True)
    except GhostCredentials.EncryptionError as e:
        logging.error(e)
        exit(1)

    config = GhostConfig()

    if args.listen:
        listeners = {
            x[0]: x[1:] if len(x) > 1 else [] for x in args.listen
        }

        config.set('ghostd', 'listen', ','.join(listeners))
        for listener in listeners:
            args = listeners[listener]
            if args:
                config.set('listeners', listener, ' '.join(args))

    ghostServer = GhostServer(config, credentials)
    ghostcmd = GhostCmdLoop(ghostServer)

    ghostServer.start()
    ghostcmd.loop()
    ghostServer.stop()
    ghostServer.finished.wait()

if __name__ == "__main__":
    main()
