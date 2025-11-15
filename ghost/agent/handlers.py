# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
__all__ = ('set_sighandlers',)

import os
import signal

import ghost.agent as ghost


logger = ghost.get_logger('signals')


def _defered_close_exit(connection):
    logger.warning('Defered close+exit')

    logger.info('Terminating client')

    ghost.client.terminate()

    logger.info('Closing connection')
    if ghost.client.connection:
        ghost.client.connection.close()

    logger.info('Done')


def _handle_sigchld(*args, **kwargs):
    os.waitpid(-1, os.WNOHANG)


def _handle_sighup(*args):
    logger.debug('SIGHUP')


def _handle_sigterm(*args):
    logger.warning('SIGTERM')

    if ghost.manager:
        try:
            ghost.manager.event(ghost.Manager.TERMINATE)
        except Exception as e:
            logger.exception(e)

    try:
        # Should be the custom event, as generated on client
        ghost.broadcast_event(0x10000000 | 0xFFFF)
        logger.info('Event broadcasted')
    except Exception as e:
        logger.exception(e)

    if ghost.client.connection:
        ghost.client.connection.defer(
            logger.exception,
            _defered_close_exit,
            ghost.client.connection
        )
    else:
        _defered_close_exit(None)

    logger.warning('SIGTERM HANDLED')


def set_sighandlers():
    if hasattr(signal, 'SIGHUP'):
        try:
            signal.signal(signal.SIGHUP, _handle_sighup)
        except Exception as e:
            logger.exception(e)

    if hasattr(signal, 'SIGTERM'):
        try:
            signal.signal(signal.SIGTERM, _handle_sigterm)
        except Exception as e:
            logger.exception(e)

    if ghost.is_supported(ghost.set_exit_session_callback):
        try:
            ghost.set_exit_session_callback(_handle_sigterm)
        except Exception as e:
            logger.exception(e)
