#!/usr/bin/env python

from module.logger import Logger
logger = Logger(__name__)

def function_a():
    logger.debug('Executing function_a')
