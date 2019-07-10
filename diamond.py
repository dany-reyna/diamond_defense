"""diamond module

Diamond Defense is a network scanner that can discover which devices are connected to a Wi-Fi network.
It gives full device details including IP address, MAC address, Vendor, and Device Name.
The user may also block devices and pause their Internet connection.

Diamond Defense can be executed with the following command line options
    start interactive mode
        sudo python3 diamond.py
    specify an interface
        sudo python3 diamond.py -i
        sudo python3 diamond.py --interface ens33
    specify packets to send per minute
        sudo python3 diamond.py -p 60
        sudo python3 diamond.py --packets 25
    display active hosts and exit
        sudo python3 diamond.py -s
        sudo python3 diamond.py --scan
    start non-interactive mode specifying target ips
        sudo python3 diamond.py -t 192.168.1.114
        sudo python3 diamond.py --target 192.168.1.242 192.168.1.237
"""

from logger import create_logger
from check_internet import is_connected
from constants import BANNER, EXAMPLES, MAX_PACKETS, MIN_PACKETS, NAME, PACKETS_PER_MIN, PATRICK, REQUIREMENTS, VERSION
from is_root import is_root
from shutdown import shutdown
from terminal_control import Color
from argparse import ArgumentParser, RawDescriptionHelpFormatter, ArgumentTypeError

log = create_logger(__name__)

try:
    from addresses import Addresses
    from display_scan import display_scan
    from interactive import interactive
    from non_interactive import non_interactive
except ModuleNotFoundError as e:
    print(f'{Color.B_RED}Requerimientos no satisfechos: {e.name}{Color.OFF}')
    print(f'{Color.B_YELLOW}Los paquetes requeridos son: {REQUIREMENTS}{Color.OFF}')
    log.exception(f'ModuleNotFoundError on {__name__} module')
    shutdown(True)


def _range_type(string):
    try:
        value = int(string)
    except ValueError:
        raise ArgumentTypeError(f"invalid int value: '{string}'")
    if MIN_PACKETS <= value <= MAX_PACKETS:
        return value
    else:
        raise ArgumentTypeError(f'invalid choice: {string} (choose from [{MIN_PACKETS}-{MAX_PACKETS}])')


def _add_args():
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter, epilog=f'{EXAMPLES}\n{PATRICK}')
    parser.add_argument('--version', action='version', version=f'{NAME} {VERSION}')
    parser.add_argument('-i', '--interface', help='interface to send packets from')
    parser.add_argument('-p', '--packets', default=PACKETS_PER_MIN,
                        type=_range_type, metavar=f'[{MIN_PACKETS}-{MAX_PACKETS}]',
                        help=f'packets to send per minute (default: {PACKETS_PER_MIN})')
    parser.add_argument('-s', '--scan', action='store_true', help='scan your network and exit')
    parser.add_argument('-t', '--target', nargs='+', help='IP address(es) to block')
    return parser.parse_args()


def _show_banner():
    print(f'{Color.B_CYAN}{BANNER}\n{" " * 28}{Color.B_RED}Version: {Color.WHITE}{VERSION}{Color.OFF}\n')


if __name__ == '__main__':
    log.debug('Adding command line interface args')
    args = _add_args()
    if is_root() and is_connected():
        log.debug('Showing banner')
        _show_banner()

        log.debug(f'Argument interface specified: {args.interface}')
        log.debug(f'Argument packets specified: {args.packets}')
        log.debug(f'Argument scan specified: {args.scan}')
        log.debug(f'Argument targets specified: {args.target}')

        if args.scan:
            log.debug('Scan selected')
            display_scan(Addresses(args.interface))
        elif args.target:
            log.debug('Non-interactive mode selected')
            try:
                non_interactive(Addresses(args.interface, False), args.packets, args.target)
            except KeyboardInterrupt:
                log.debug(f'KeyboardInterrupt on {__name__} module')
        else:
            log.debug('Interactive mode selected')
            try:
                interactive(Addresses(args.interface), args.packets)
            except KeyboardInterrupt:
                log.debug(f'KeyboardInterrupt on {__name__} module')
    else:
        shutdown(True)
