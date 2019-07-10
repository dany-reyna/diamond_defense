"""scan module

This module exports:
  - Host                dataclass containing host ip, mac, vendor and hostname
  - scan                function that returns a list of active hosts
"""
from logger import create_logger
from mac_vendor import get_vendor
from shutdown import shutdown
from terminal_control import Color
from dataclasses import dataclass
from nmap import nmap, PortScannerError

log = create_logger(__name__)


@dataclass(frozen=True)
class Host:
    """Dataclass containing host ip, mac, vendor and hostname"""
    ip: str
    mac: str
    vendor: str
    hostname: str
    __slots__ = ('ip', 'mac', 'vendor', 'hostname')


def scan(ip):
    """Scan `ip` for active hosts with `nmap -sn` (no port scan)

    :param ip: String specifying nmap targets e.g. 'scanme.nmap.org', '198.116.0-255.1-127', '216.163.128.20/20'
    :return: List of active hosts with their respective ip, mac, vendor and hostname
    :exception KeyError: If 'mac' is not in the 'addresses' dict. This happens with localhost and gets skipped
    :exception PortScannerError: If nmap is not found in the path
    :exception KeyboardInterrupt: If the user interrupts the program (⌃C)
    """
    log.debug('Scan starting')
    hosts = []
    scanner = _get_scanner()
    if scanner:
        result_dict = _get_scan_result(scanner, ip)
        for k, v in result_dict['scan'].items():
            if v['status']['state'] == 'up':
                log.debug(f'{v} is up')
                try:
                    mac = v['addresses']['mac']
                except KeyError:
                    log.debug(f'KeyError on {__name__} module. Localhost response.')
                    continue
                ip = v['addresses']['ipv4']
                vendor = v['vendor'][mac] if v['vendor'] else get_vendor(mac)
                hostname = v['hostnames'][0]['name'] or 'N/A'
                hosts.append(Host(ip, mac, vendor, hostname))
    return hosts


def _get_scanner():
    try:
        return nmap.PortScanner()
    except PortScannerError:
        print(f'{Color.B_RED}No se encontró nmap instalado{Color.OFF}')
        log.exception(f'PortScannerError on {__name__} module')
        shutdown(True)


def _get_scan_result(scanner, host):
    try:
        return scanner.scan(hosts=host, arguments='-sn')
    except KeyboardInterrupt:
        log.debug(f'KeyboardInterrupt on {__name__} module')
        shutdown()
