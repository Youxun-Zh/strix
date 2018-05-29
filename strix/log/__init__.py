"""
"""

import logging

from .log import generate_streaming_handler, generate_logger


streaming_handler = generate_streaming_handler()
app_log = generate_logger(streaming_handler, logging.INFO)
