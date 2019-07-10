"""addresses module

This module exports:
  - Interface       dataclass containing interface name and mac
  - Gateway         dataclass containing gateway ip and mac
  - Network         dataclass containing network ip and subnet mask
  - Addresses       class that gets information about the interface, gateway and network
"""

from logger import create_logger
from constants import PROMPT
from scan import scan
from shutdown import shutdown
from terminal_control import Color
from dataclasses import dataclass
import netifaces
from kamene.config import conf
from kamene.utils import ltoa

log = create_logger(__name__)


@dataclass
class Interface:
    """Dataclass containing interface name and mac"""
    name: str
    mac: str
    __slots__ = ('name', 'mac')


@dataclass
class Gateway:
    """Dataclass containing gateway ip and mac"""
    ip: str
    mac: str
    __slots__ = ('ip', 'mac')


@dataclass
class Network:
    """Dataclass containing network ip and subnet mask"""
    ip: str
    mask: str
    cidr: str
    __slots__ = ('ip', 'mask', 'cidr')


class Addresses:
    """Get information about the interface, gateway and network

        Public methods:
          - sync        Reassign interface, gateway and network
    """
    __slots__ = ('interface', 'gateway', 'network', 'interface_input', 'interactive')

    def __init__(self, interface_name=None, interactive=True):
        """An Address object that gets information about the interface, gateway and network

        :param interface_name: Optionally specify the interface name. Default: None
        :param interactive: Boolean value. If True user prompt is allowed. Default: True
        """
        self.interface = Interface('', '')
        self.gateway = Gateway('', '')
        self.network = Network('', '', '')
        self.interface_input = interface_name
        self.interactive = interactive
        self.sync()
        log.debug(f'Addresses created: {self!r}')

    def sync(self):
        """Reassign interface, gateway and network data

        :exception KeyError: If the default gateway is not found
        :exception KeyboardInterrupt: If the user interrupts the program (⌃C)
        :exception EOFError: If the user enters EOF (⌃D)
        :exception StopIteration: If the interface name is not found
        :exception IndexError: If the scan's list of hosts is empty because the gateway IP is not active
        """
        log.debug('Getting gateway ip and interface name')
        self._gateway_ip_interface_name()
        log.debug('Getting gateway mac')
        self._gateway_mac()
        log.debug('Getting interface mac')
        self._interface_mac()
        log.debug('Getting network ip and mask')
        self._network_ip_mask()

    def _gateway_ip_interface_name(self):
        if self.interface_input:
            log.debug(f'Getting from input: {self.interface_input}')
            self.interface.name = self.interface_input
            self._gateway_ip_from_interface_input()
        else:
            try:
                self.gateway.ip, self.interface.name = netifaces.gateways()['default'][netifaces.AF_INET]
            except KeyError:
                print(f'{Color.B_YELLOW}Hubo un problema al obtener la interfaz.{Color.OFF}')
                log.exception(f'KeyError on {__name__} module')
                if self.interactive:
                    log.debug('Displaying user prompt')
                    self._interface_prompt()
                    self._gateway_ip_from_interface_input()
                else:
                    shutdown(True)

    def _interface_prompt(self):
        try:
            self.interface.name = input(f'{Color.B_GREEN}Ingresa el nombre de la interfaz de red '
                                        f'(p.ej. en0, ens33, eth0)'
                                        f'\n{Color.CYAN}{PROMPT}{Color.OFF}')
        except KeyboardInterrupt:
            log.debug(f'KeyboardInterrupt on {__name__} module')
            shutdown()
        except EOFError:
            log.debug(f'EOFError on {__name__} module')
            shutdown()

    def _gateway_ip_from_interface_input(self):
        gateways = netifaces.gateways()[netifaces.AF_INET]
        try:
            # At [0] because each entry is an (address, interface, is_default) tuple
            self.gateway.ip = next(g[0] for g in gateways if self.interface.name in g)
        except StopIteration:
            print(f'{Color.B_RED}No se pudo obtener la dirección gateway con la interfaz ingresada{Color.OFF}')
            log.exception(f'StopIteration on {__name__} module')
            shutdown(True)

    def _gateway_mac(self):
        try:
            self.gateway.mac = scan(self.gateway.ip)[0].mac
        except IndexError:
            print(f'{Color.B_RED}No se pudo obtener la MAC del gateway{Color.OFF}')
            log.exception('Could not get gateway MAC')
            shutdown(True)

    def _interface_mac(self):
        # At [0]['addr'] because it is a [{'addr': 'XX:XX:XX:XX:XX:XX'}] list
        self.interface.mac = netifaces.ifaddresses(self.interface.name)[netifaces.AF_LINK][0]['addr']

    def _network_ip_mask(self):
        # Routes is network, net mask, gateway, interface, output IP
        interface_routes = [r for r in conf.route.routes if r[3] == self.interface.name and r[1] != 0xFFFFFFFF]

        # Longest prefix match: the most specific of the matching table entries, the one with the longest subnet mask
        net, msk, _, _, _ = max(interface_routes, key=lambda i: i[1])

        self.network.ip = ltoa(net)
        self.network.mask = ltoa(msk)
        self.network.cidr = f'{self.network.ip}/{bin(msk).count("1")}'

    def __repr__(self):
        class_name = self.__class__.__name__
        args = [f'{self.interface!r}', f'{self.gateway!r}', f'{self.network!r}',
                f'{self.interface_input!r}', f'{self.interactive!r}']
        return f'{class_name}({", ".join(args)})'
