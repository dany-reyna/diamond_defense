"""non_interactive module

This module exports:
  - non_interactive     function that enters Diamond Defense on non-interactive mode
"""
from logger import create_logger
from display_block import display_block
from loading_animation import animate
from scan import scan
from terminal_control import Color
from shutdown import shutdown
import re

log = create_logger(__name__)


def non_interactive(addresses, packets, ips):
    """Enter Diamond Defense on non-interactive mode

    Validate the given ips.
    Display interface, gateway ip and target ips.
    Check if the target ips are active.
    Start blocking.

    :param addresses: An Addresses object
    :param packets: Packets to send per minute
    :param ips: The target IPs to block
    :exception KeyboardInterrupt: If the user interrupts the program (⌃C)
    :exception IndexError: If the scan's list of hosts is empty because the specified IP is not active
    """
    log.debug('Validating ips')
    _validate(ips)
    log.debug('Displaying interface, gateway ip and target ips')
    _display_info(addresses, ips)

    print(f'\n{Color.B_CYAN}Bloquear dispositivos (modo no interactivo) {Color.B_GREEN}seleccionado...{Color.OFF}')

    log.debug('Checking status of target ips')
    targets = _check_status(ips)

    if targets:
        display_block(targets, addresses, packets)
    else:
        print(f'{Color.B_RED}Ninguno de los objetivos está activo{Color.OFF}')
        log.error('No active targets')
        shutdown(True)


def _validate(ips):
    ip_pattern = re.compile('^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}'
                            '(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$')
    for i in ips:
        if not ip_pattern.match(i):
            print(f'{Color.B_RED}{i} no es una dirección IP válida{Color.OFF}')
            log.error(f'Not a valid IP: {i}')
            shutdown(True)


def _display_info(addresses, targets):
    print(f'👩🏻‍💻 {Color.CYAN}Utilizando interfaz {Color.MAGENTA}{addresses.interface.name}'
          f'{Color.CYAN} con dirección MAC {Color.MAGENTA}{addresses.interface.mac}{Color.OFF}')
    print(f'📡 {Color.CYAN}Router: {Color.MAGENTA}{addresses.gateway.ip}'
          f'{Color.CYAN} --> Objetivo(s): {Color.B_RED}{", ".join(targets)}{Color.OFF} 📱 🖥  📺 🕹️')


@animate(msg=f'{Color.B_YELLOW}Revisando el estado de los objetivos, espera un momento...')
def _check_status(ips):
    targets = []
    for ip in ips:
        try:
            targets.append(scan(ip)[0])
        except IndexError:
            print(f'{Color.B_RED}El objetivo {ip} no parece estar activo. Omitiendo...{Color.OFF}')
            log.error(f'Not active: {ip}')
    return targets
