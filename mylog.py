#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

__author__ = 'lycheng'
__email__ = "lycheng997@gmail.com"
__date__ = '2014-01-23'

import logging
import logging.handlers

LoggingLevel = logging.DEBUG
LOG_PATH = 'log/status.log'

def setup_logger(logger):
    """
    Set up a specific logger - logger
    """
    logger.setLevel(LoggingLevel)
    log_path = LOG_PATH
    handler = logging.handlers.TimedRotatingFileHandler(log_path, when='d', interval=1)
    handler.setLevel(LoggingLevel)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


logger = logging.getLogger('error')
setup_logger(logger)
