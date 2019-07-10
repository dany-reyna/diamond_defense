"""is_root module

This module exports:
  - is_root     function that returns whether user is root
"""

from logger import create_logger
from terminal_control import Color
import os

log = create_logger(__name__)


def is_root():
    """Checks whether user is root

    The superuser normally has a UID of zero (0).

    :return: True if user is root, else False
    :exception AttributeError: If the OS isn't UNIX-like
    """
    try:
        euid = os.geteuid()
    except AttributeError:
        print(f'{Color.B_YELLOW}¿Estás en Windows? Diamond Defense sólo funciona en sistemas UNIX{Color.OFF}')
        log.exception(f'AttributeError on {__name__} module')
        return False

    if euid == 0:
        log.debug('User is root')
        return True
    else:
        print(f'{Color.B_RED}Diamond Defense debe correr con privilegios de superusuario. Intenta con:{Color.OFF}')
        print(f'{Color.B_GREEN}sudo python3 diamond.py{Color.OFF}')
        log.error('User is not root')
        return False
