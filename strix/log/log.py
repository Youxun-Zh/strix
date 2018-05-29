"""
    strix.log

    
"""

import logging
import sys

LOG_FROMAT = "%(asctime)-15s %(clientip)s %(user)-8s %(message)s"


def generate_streaming_handler():
# def generate_streaming_handler(handler_class, *args, **kwargs):
    # try:
    #     handler = getattr(logging, handler_class, args, kwargs)
    # except AttributeError:
    #     handler = getattr(logging.handlers, handler_class, args, kwargs)
    # except AttributeError:
    #     raise()
    handler = logging.StreamHandler(sys.stdout)
    return handler


def generate_logger(handler, level=logging.DEBUG):
    handler = logging.StreamHandler(sys.stdout)
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger
