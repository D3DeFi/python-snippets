#!/usr/bin/env python

import argparse
from module.a import function_a
from module.b import function_b
from module.logger import Logger


if __name__ == '__main__':
    logger = Logger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', help='debug level to use')
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(args.debug)

    logger.info('Running imported functions...')
    for function in [function_a, function_b]:
        function()
    logger.info('Run complete.')
    logger.info('Exiting...')
