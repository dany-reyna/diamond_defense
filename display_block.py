"""display_block module

This module exports:
  - display_block       function that displays targets, blocks them and restores the connection when
                        the user interrupts the program (⌃C)
"""
from logger import create_logger
from block import block, restore_connection
from terminal_control import Color

log = create_logger(__name__)


def display_block(targets, addresses, packets):
    """Display targets, block them and restore the connection when the user interrupts the program (⌃C)

    :param targets: List of target hosts
    :param addresses: An Addresses object
    :param packets: Packets to send per minute
    :exception KeyboardInterrupt: If the user interrupts the program (⌃C)
    """
    log.debug('Displaying targets')
    ips = [t.ip for t in targets]
    print(f'\n{Color.B_CYAN}Objetivo(s): {Color.WHITE}{", ".join(ips)}{Color.OFF}')

    print(f'{Color.B_CYAN}Bloqueo iniciado ( {Color.WHITE}{packets} paquetes/minuto {Color.B_CYAN}){Color.OFF}')
    print(f'\n{Color.MAGENTA}Para detener el bloqueo, presiona ^C{Color.OFF}')

    log.debug('Starting block')
    try:
        block(targets, addresses, packets)
    except KeyboardInterrupt:
        restore_connection(targets, addresses)
        print(f'{Color.B_GREEN}Conexión restaurada con éxito{Color.OFF}')
        log.debug(f'KeyboardInterrupt on {__name__} module')
        log.debug('Block stopped')
