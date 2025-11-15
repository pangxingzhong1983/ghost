# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging

logger = logging.getLogger('ghost')
def getLogger(name):
    return logger.getChild(name)
