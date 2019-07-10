"""loading_animation module

This module exports:
  - animate             decorator for displaying an animation when calling a function
  - LoadingThread       threading.Thread subclass that displays a loading text animation
"""

from logger import create_logger
from terminal_control import Color
import threading
import time

log = create_logger(__name__)


def animate(msg='Loading...'):
    """Decorator for displaying an animation when calling a function

    :param msg: Message to display with the animation. Default: 'Loading...'
    :return: Decorator that calls the inner function
    """

    def real_decorator(func):
        """The real decorator. Outer decorator is used for taking an argument

        :param func: The function to call
        :return: The wrapper that adds animation to the function
        """

        def wrapper(*args, **kwargs):
            animation = LoadingThread(msg)
            animation.start()
            result = func(*args, **kwargs)
            animation.stop()
            return result

        return wrapper

    return real_decorator


class LoadingThread(threading.Thread):
    """threading.Thread subclass that displays a loading text animation

        Output can be customized with the msg property

        Public methods:
          - run     overridden from threading.Thread to display a loading text animation
          - stop    stop the running animation
    """
    __slots__ = ('msg', '_loading')

    def __init__(self, msg):
        """A LoadingThread object (daemon thread) used for displaying a loading text animation

        :param msg: Message to display with the animation.
        """
        super().__init__()
        self.daemon = True
        self.msg = msg
        self._loading = True
        log.debug(f'LoadingThread created: {self!r}')

    def run(self):
        """Overridden from threading.Thread to display a loading text animation"""
        animation = r'\|/—'
        i = 0
        log.debug(f'LoadingThread running: {self!r}')
        print()  # print message on its own line
        while self._loading:
            print(f'{self.msg} {animation[i % len(animation)]}{Color.OFF}', end='\r')
            i += 1
            time.sleep(0.1)

    def stop(self):
        """Stop the running animation"""
        self._loading = False
        print(end='\n\n')  # get space after message
        log.debug(f'LoadingThread stopping: {self!r}')

    def __repr__(self):
        class_name = self.__class__.__name__
        args = [f'{self.msg!r}', f'{self._loading!r}']
        return f'{class_name}({", ".join(args)})'
