"""check_internet

This module exports:
  - is_connected      function that verifies there is an active internet connection
"""
from logger import create_logger
from shutdown import shutdown
from terminal_control import Color
from urllib.parse import urlsplit, quote_plus
from urllib.request import Request, urlopen
from urllib.error import URLError

log = create_logger(__name__)


def is_connected(site='https://github.com', timeout=5):
    """Try to connect to `site` with a specified `timeout`
       Show an error if the connection fails or if there's an error parsing the site url

    :param site: The website to connect to. Default: 'https://github.com'
    :param timeout: The connection timeout in seconds. Default: 5
    :return: True if there's internet. False otherwise
    :exception ValueError: If an invalid port is specified in the URL.
    Or if there are unmatched square brackets in the netloc attribute
    :exception UnicodeEncodeError: If the URL has a character unsupported by the default utf-8 encoding
    :exception URLError: If the URL can't be opened
    :exception KeyboardInterrupt: If the user interrupts the program (⌃C)
    """
    log.debug(f'Connecting to {site} with a {timeout} second timeout')
    request = _parse_url(site)
    try:
        with urlopen(request, timeout=timeout) as response:
            log.debug(f'Got response {response}')
            return True
    except URLError:
        print(f'{Color.B_RED}Al parecer no estás en linea. Por favor revisa tu conexión a Internet.{Color.OFF}')
        log.exception(f'URLError on {__name__} module')
        return False
    except KeyboardInterrupt:
        log.debug(f'KeyboardInterrupt on {__name__} module')
        shutdown()


def _parse_url(site):
    split_result = _split(site)
    log.debug(f'Split result: {split_result}')

    log.debug('Verifying that url scheme is https')
    _verify_https(split_result.scheme)

    quoted = _quote(split_result.netloc)
    log.debug(f'Quoted special characters and non-ASCII text: {quoted}')

    url = f'{split_result.scheme}://{quoted}'
    log.debug(f'Parsed url: {url}')
    return Request(url)


def _split(site):
    try:
        return urlsplit(site)
    except ValueError:
        print(f'{Color.B_RED}Hubo un error analizando la URL: {site}{Color.OFF}')
        log.exception(f'ValueError on {__name__} module')
        shutdown(True)


def _verify_https(scheme):
    if scheme != 'https':
        print(f'{Color.B_RED}El esquema de la URL debe ser https, es: {scheme}{Color.OFF}')
        log.error(f'Not an https scheme: {scheme}')
        shutdown(True)


def _quote(netloc):
    try:
        return quote_plus(netloc)
    except UnicodeEncodeError:
        print(f'{Color.B_RED}Hay un caracter no válido en la URL{Color.OFF}')
        log.exception(f'UnicodeEncodeError on {__name__} module')
        shutdown(True)
