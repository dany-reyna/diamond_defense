"""mac_vendor module

This module exports:
  - get_vendor      function that gets the vendor name from a MAC address
"""
from logger import create_logger
from constants import MAC_VENDORS_API
from shutdown import shutdown
from terminal_control import Color
from urllib.request import urlopen
from urllib.error import URLError

log = create_logger(__name__)


def get_vendor(mac):
    """Return the vendor name given a `mac` address

    :param mac: The MAC address to get the vendor from
    :return: The vendor name from the given MAC address.
    'Please provide mac address' if the mac parameter is empty.
    'No vendor' if the vendor name could not be found.
    'N/A' if there was an error accessing the API.
    :exception URLError: If there is no connection
    :exception KeyboardInterrupt: If the user interrupts the program (⌃C)
    """
    try:
        with urlopen(f'{MAC_VENDORS_API}{mac}') as response:
            vendor = response.read().decode()
            log.debug(f'Got vendor {vendor}')
            return vendor
    except URLError:
        print(f'{Color.B_RED}No se pudo obtener el nombre del fabricante{Color.OFF}')
        log.exception(f'URLError on {__name__} module')
        return 'N/A'
    except KeyboardInterrupt:
        log.debug(f'KeyboardInterrupt on {__name__} module')
        shutdown()
