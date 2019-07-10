"""interactive module

This module exports:
  - interactive         function that enters Diamond Defense on interactive mode
"""

from logger import create_logger
from constants import PROMPT
from display_block import display_block
from display_scan import display_network_info, display_hosts, get_hosts
from shutdown import shutdown
from terminal_control import Color, Misc
import time
import re

log = create_logger(__name__)


def interactive(addresses, packets):
    """Enter Diamond Defense on interactive mode

    Display network information.
    Display options.
    Ask user for targets.
    Start blocking.

    :param addresses: An Addresses object
    :param packets: Packets to send per minute
    :exception KeyboardInterrupt: If the user interrupts the program (⌃C)
    :exception EOFError: If the user enters EOF (⌃D)
    :exception ValueError: If the user enters not a number when selecting a target
    :exception IndexError: If the user enters a target number not available
    """
    hosts = get_hosts(addresses)
    display_network_info(hosts, addresses)

    pattern_block = re.compile('^b(lock)?$')
    pattern_clear = re.compile('^cl(ear)?$')
    pattern_exit = re.compile('^e(xit)?$')
    option = ''
    while True:
        _display_options()
        try:
            option = input(f'\n{Color.CYAN}{PROMPT}{Color.OFF}').lower()
        except KeyboardInterrupt:
            log.debug(f'KeyboardInterrupt on {__name__} module')
            shutdown()
        except EOFError:
            log.debug(f'EOFError on {__name__} module')
            shutdown()

        if pattern_block.match(option):
            log.debug('Selected: block')
            _choose_targets(addresses, packets)
        elif pattern_clear.match(option):
            log.debug('Selected: clear')
            print(f'{Misc.CLEAR}')
        elif pattern_exit.match(option):
            log.debug('Selected: exit')
            shutdown()
        else:
            log.debug('Selected: invalid option')
            print(f'{Color.B_YELLOW}Ingresa una opción válida.{Color.OFF}')


def _display_options():
    options = [f'\n{Color.CYAN}Elige una opción\n',
               f'   {Color.WHITE}[{Color.GREEN}b/block{Color.WHITE}]\t{Color.BLUE} Bloquear dispositivos',
               f'   {Color.WHITE}[{Color.GREEN}cl/clear{Color.WHITE}]\t{Color.BLUE} Limpiar pantalla',
               f'   {Color.WHITE}[{Color.GREEN}e/exit{Color.WHITE}]\t{Color.BLUE} Salir de Diamond Defense{Color.OFF}']
    log.debug('Displaying options')
    for o in options:
        print(o)
        time.sleep(0.1)


def _choose_targets(addresses, packets):
    print(f'{Misc.CLEAR}')
    print(f'{Color.B_CYAN}Bloquear dispositivos (modo interactivo) {Color.B_GREEN}seleccionado...{Color.OFF}')

    log.debug('Getting addresses')
    addresses.sync()

    hosts = get_hosts(addresses)
    display_hosts(hosts)

    log.debug('Asking user for targets')
    targets = _parse_targets(_get_target_numbers(), hosts, addresses)

    if targets:
        display_block(targets, addresses, packets)
    else:
        print(f'{Color.B_RED}No seleccionaste ningún dispositivo de la lista{Color.OFF}')
        log.warning('No valid target(s) selected')


def _get_target_numbers():
    list_with_empty_elements = [t.strip() for t in _targets_prompt().split(',')]
    return [i for i in list_with_empty_elements if i]


def _targets_prompt():
    try:
        return input(f'\n{Color.B_GREEN}Elige los dispositivos a bloquear (separados por coma)'
                     f'\n{Color.CYAN}{PROMPT}{Color.OFF}')
    except KeyboardInterrupt:
        log.debug(f'KeyboardInterrupt on {__name__} module')
        shutdown()
    except EOFError:
        log.debug(f'EOFError on {__name__} module')
        shutdown()


def _parse_targets(target_numbers, hosts, addresses):
    targets = []
    for i in target_numbers:
        try:
            i = int(i)
        except ValueError:
            print(f'{Color.B_YELLOW}{i} no está en la lista{Color.OFF}')
            log.exception(f'ValueError on {__name__} module')
            continue

        try:
            host = hosts[i]
        except IndexError:
            print(f'{Color.B_YELLOW}{i} no está en la lista{Color.OFF}')
            log.exception(f'IndexError on {__name__} module')
            continue

        if host.ip == addresses.gateway.ip:
            print(f'{Color.B_YELLOW}{host.ip} es tu router/modem, no puedes bloquearlo{Color.OFF}')
            log.warning('Gateway IP selected')
            continue
        else:
            targets.append(host)
            log.debug(f'Appended {host}')
    return targets
