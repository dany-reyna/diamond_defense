"""terminal_control module

This module exports:
  - Color       Enumeration with ANSI escape sequences that set color screen attributes
  - Misc        Enumeration with ANSI escape sequences that control other screen attributes such as cursor and erasing

Syntax:
    Esc[<Value>;...;<Value>m

The \033 represents an escape

The "m" sets graphics mode:
    Calls the graphics functions specified by the following values.
    These specified functions remain active until the next occurrence of this escape sequence.
    Graphics mode changes the colors and attributes of text (such as bold and underline) displayed on the screen.

        Text attributes
        0	All attributes off
        1	Bold on
        4	Underscore (on monochrome display adapter only)
        5	Blink on
        7	Reverse video on
        8	Concealed on

        Name            FG Code     BG Code
        Black           30	        40
        Red             31          41
        Green	        32          42
        Yellow	        33          43
        Blue	        34          44
        Magenta	        35          45
        Cyan	        36          46
        White	        37          47
        Bright Black    90          100
        Bright Red      91          101
        Bright Green    92          102
        Bright Yellow   93          103
        Bright Blue     94          104
        Bright Magenta  95          105
        Bright Cyan     96          106
        Bright White    97          107

Cursor Control
    Cursor Home     Esc[<row>;<column>H
        Sets the cursor position where subsequent text will begin.
        If no row/column parameters are provided (ie. <ESC>[H), the cursor will move to the home position,
        at the upper left of the screen.

Erasing Text
    Erase Down      Esc[J
        Erases the screen from the current line down to the bottom of the screen.

More info:
    http://ascii-table.com/ansi-escape-sequences.php
    https://en.wikipedia.org/wiki/ANSI_escape_code#3/4_bit
    http://www.termsys.demon.co.uk/vtansi.htm
"""

from enum import Enum, unique


@unique
class Color(Enum):
    """Enumeration for 'colorizing' console output

    :raises: AttributeError
    """
    OFF = '\033[0m'
    GREEN = '\033[32m'
    B_GREEN = '\033[1;32m'
    MAGENTA = '\033[35m'
    B_RED = '\033[1;91m'
    B_YELLOW = '\33[1;93m'
    BLUE = '\33[94m'
    CYAN = '\33[96m'
    B_CYAN = '\33[1;96m'
    WHITE = '\33[97m'
    B_WHITE = '\33[1;97m'

    def __str__(self):
        return self.value


@unique
class Misc(Enum):
    """Enumeration for other terminal control operations

    :raises: AttributeError
    """
    CLEAR = '\033[H\033[J'

    def __str__(self):
        return self.value
