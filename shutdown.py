"""shutdown module

This module exports:
  - shutdown        function that exits execution
"""

from logger import create_logger
from terminal_control import Color
import sys

log = create_logger(__name__)


def shutdown(error=False):
    """Exit the python interpreter

    :param error: If True exits with status one (i.e., failure). Default: False
    """
    if error:
        log.error('Error shutdown')
        sys.exit(1)
    else:
        print(f'\n{Color.B_GREEN}¡Nos vemos! :D{Color.OFF}')
        log.debug('Normal shutdown')
        sys.exit()
