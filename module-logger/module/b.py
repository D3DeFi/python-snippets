#!/usr/bin/env python

from module.logger import Logger
logger = Logger(__name__)

def function_b():
    logger.debug('Executing function_b')
