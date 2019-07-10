"""display_scan module

This module exports:
  - display_scan                function that scans and displays information about the network and its active hosts
  - display_network_info        function that displays information about the network
  - display_hosts               function that displays information about the hosts
  - get_hosts                   function that scans the network, validates that hosts are active and returns them
"""
from logger import create_logger
from loading_animation import animate
from scan import scan
from shutdown import shutdown
from terminal_control import Color

log = create_logger(__name__)


def display_scan(addresses):
    """Perform a scan and display information about the network and its active hosts

    :param addresses: An Addresses object
    """
    hosts = get_hosts(addresses)
    display_network_info(hosts, addresses)
    display_hosts(hosts)


def display_network_info(hosts, addresses):
    """Display information about the network

    :param hosts: A list of Host objects
    :param addresses: An Addresses object
    """
    log.debug('Displaying network information')
    print(f'👩🏻‍💻 {Color.CYAN}Utilizando interfaz {Color.MAGENTA}{addresses.interface.name}'
          f'{Color.CYAN} con dirección MAC {Color.MAGENTA}{addresses.interface.mac}{Color.OFF}')
    print(f'📡 {Color.CYAN}Router: {Color.MAGENTA}{addresses.gateway.ip}'
          f'{Color.CYAN} --> {Color.B_RED}{len(hosts)} {Color.CYAN}dispositivos activos{Color.OFF} 📱 🖥  📺 🕹️')


def display_hosts(hosts):
    """Display information about the hosts

    :param hosts: A list of Host objects
    """
    log.debug('Displaying active hosts')
    print(f'\n{Color.B_WHITE}Dispositivos conectados:{Color.OFF}')
    for index, host in enumerate(hosts):
        print(f'  {Color.WHITE}[{Color.GREEN}{index}{Color.WHITE}] {Color.BLUE}{host.ip}\t\t{host.mac}'
              f'\t{Color.CYAN}{host.vendor} ({Color.MAGENTA}{host.hostname}{Color.CYAN}){Color.OFF}')


def get_hosts(addresses):
    """Scan network, validate that hosts are active and return them

    :param addresses: An Addresses object
    :return: List of active hosts with their respective ip, mac, vendor and hostname
    """
    log.debug('Getting hosts')
    hosts = _scan_network(addresses)
    _check_hosts_length(hosts, addresses)
    return hosts


@animate(msg=f'{Color.B_YELLOW}Escaneando tu red, espera un momento...')
def _scan_network(addresses):
    return scan(addresses.network.cidr)


def _check_hosts_length(hosts, addresses):
    if len(hosts) == 1 and hosts[0].ip == addresses.gateway.ip:
        print(f'{Color.B_RED}El único host activo es el router/modem. No hay nadie a quién bloquear.{Color.OFF}')
        log.error('Only gateway is active')
        shutdown(True)
    elif len(hosts) == 0:
        print(f'{Color.B_RED}No hay hosts activos en tu red. Algo salió mal.{Color.OFF}')
        log.error('No active hosts')
        shutdown(True)
