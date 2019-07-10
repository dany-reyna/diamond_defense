"""logger module

This module exports:
  - create_logger   function that returns a logger for console and file output
"""

import logging
from pathlib import Path


def create_logger(name):
    """Create a logger for console and file output

    :param name: The name of the module to log
    :return: A logger with the specified name
    """

    # Get logger module's dir and create 'logs' directory if it doesn't exist
    output_dir = Path(__file__).resolve().parent / 'logs'
    output_dir.mkdir(exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create console and file handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(output_dir / f'{name}.log')
    c_handler.setLevel(logging.WARNING)
    f_handler.setLevel(logging.DEBUG)

    # Set formats
    c_format = logging.Formatter('%(levelname)s - %(name)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(levelname)s\t- %(name)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers
    # logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger
