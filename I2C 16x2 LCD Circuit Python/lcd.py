# Copyright (C) 2017 Dan Halbert
# Adapted from https://github.com/dbrgn/RPLCD, Copyright (C) 2013-2016 Danilo Bargen

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import time
from micropython import const

# Commands
_LCD_CLEARDISPLAY = const(0x01)
_LCD_RETURNHOME = const(0x02)
_LCD_ENTRYMODESET = const(0x04)
_LCD_DISPLAYCONTROL = const(0x08)
_LCD_CURSORSHIFT = const(0x10)
_LCD_FUNCTIONSET = const(0x20)
_LCD_SETCGRAMADDR = const(0x40)
_LCD_SETDDRAMADDR = const(0x80)

# Flags for display entry mode
_LCD_ENTRYRIGHT = const(0x00)
_LCD_ENTRYLEFT = const(0x02)
_LCD_ENTRYSHIFTINCREMENT = const(0x01)
_LCD_ENTRYSHIFTDECREMENT = const(0x00)

# Flags for display on/off control
_LCD_DISPLAYON = const(0x04)
_LCD_DISPLAYOFF = const(0x00)
_LCD_CURSORON = const(0x02)
_LCD_CURSOROFF = const(0x00)
_LCD_BLINKON = const(0x01)
_LCD_BLINKOFF = const(0x00)

# Flags for display/cursor shift
_LCD_DISPLAYMOVE = const(0x08)
_LCD_CURSORMOVE = const(0x00)
_LCD_MOVERIGHT = const(0x04)
_LCD_MOVELEFT = const(0x00)

# Flags for function set
_LCD_8BITMODE = const(0x10)
LCD_4BITMODE = const(0x00)
_LCD_2LINE = const(0x08)
_LCD_1LINE = const(0x00)
_LCD_5x10DOTS = const(0x04)
_LCD_5x8DOTS = const(0x00)

# Flags for backlight control
LCD_BACKLIGHT = const(0x08)
LCD_NOBACKLIGHT = const(0x00)

# Flags for RS pin modes
_RS_INSTRUCTION = const(0x00)
_RS_DATA = const(0x01)

# Pin bitmasks
PIN_ENABLE = const(0x4)
PIN_READ_WRITE = const(0x2)
PIN_REGISTER_SELECT = const(0x1)

class CursorMode:
    HIDE = const(_LCD_CURSOROFF | _LCD_BLINKOFF)
    LINE = const(_LCD_CURSORON | _LCD_BLINKOFF)
    BLINK = const(_LCD_CURSOROFF | _LCD_BLINKON)

MICROSECOND = 1e-6
MILLISECOND = 1e-3

class LCD(object):

    def __init__(self, interface, num_cols=20, num_rows=4, char_height=8):
        """
        Character LCD controller.
        
        :param interface: Communication interface, such as I2CInterface
        :param num_rows: Number of display rows (usually 1, 2 or 4). Default: 4.
        :param num_cols: Number of columns per row (usually 16 or 20). Default 20.
        :param char_height: Some 1 line displays allow a font height of 10px.
                Allowed: 8 or 10. Default: 8.
        """
        self.interface = interface
        
        if char_height not in (8, 10):
            raise ValueError('The ``char_height`` argument should be either 8 or 10.')
        self.char_height = char_height

        self.num_rows = num_rows
        self.num_cols = num_cols
        
        # get row addresses (varies based on display size)
        self._row_offsets = (0x00, 0x40, self.num_cols, 0x40 + self.num_cols)
 
        # Setup initial display configuration
        displayfunction = self.interface.data_bus_mode | _LCD_5x8DOTS
        if self.num_rows == 1:
            displayfunction |= _LCD_1LINE
        elif self.num_rows in (2, 4):
            # LCD only uses two lines on 4 row displays
            displayfunction |= _LCD_2LINE
        if self.char_height == 10:
            # For some 1 line displays you can select a 10px font.
            displayfunction |= _LCD_5x10DOTS

        # Choose 4 or 8 bit mode
        self.command(0x03)
        time.sleep(4.5*MILLISECOND)
        self.command(0x03)
        time.sleep(4.5*MILLISECOND)
        self.command(0x03)
        if self.interface.data_bus_mode == LCD_4BITMODE:
            # Hitachi manual page 46
            time.sleep(100*MICROSECOND)
            self.command(0x02)
        elif self.interface.data_bus_mode == _LCD_8BITMODE:
            # Hitachi manual page 45
            self.command(0x30)
            time.sleep(4.5*MILLISECOND)
            self.command(0x30)
            time.sleep(100*MICROSECOND)
            self.command(0x30)
        else:
            raise ValueError('Invalid data bus mode: {}'.format(self.interface.data_bus_mode))

        # Write configuration to display
        self.command(_LCD_FUNCTIONSET | displayfunction)
        time.sleep(50*MICROSECOND)

        # Configure entry mode. Define internal fields.
        self.command(_LCD_ENTRYMODESET | _LCD_ENTRYLEFT)
        time.sleep(50*MICROSECOND)

        # Configure display mode. Define internal fields.
        self._display_mode = _LCD_DISPLAYON
        self._cursor_mode = CursorMode.HIDE
        self.command(_LCD_DISPLAYCONTROL | self._display_mode | self._cursor_mode)
        time.sleep(50*MICROSECOND)

        self.clear()

    def close(self):
        self.interface.deinit()

    def set_backlight(self, value):
        self.interface.backlight = value

    def set_display_enabled(self, value):
        self._display_mode = _LCD_DISPLAYON if value else _LCD_DISPLAYOFF
        self.command(_LCD_DISPLAYCONTROL | self._display_mode | self._cursor_mode)
        time.sleep(50*MICROSECOND)

    def set_cursor_mode(self, value):
        self._cursor_mode = value
        self.command(_LCD_DISPLAYCONTROL | self._display_mode | self._cursor_mode)
        time.sleep(50*MICROSECOND)

    def cursor_pos(self):
        """The cursor position as a 2-tuple (row, col)."""
        return (self._row, self._col)

    def set_cursor_pos(self, row, col):
        if not (0 <= row < self.num_rows):
            raise ValueError('row should be in range 0-{}'.format(self.num_rows - 1))
        if not (0 <= col < self.num_cols):
            raise ValueError('col should be in range 0-{}'.format(self.num_cols - 1))
        self._row = row
        self._col = col
        self.command(_LCD_SETDDRAMADDR | self._row_offsets[row] + col)
        time.sleep(50*MICROSECOND)

    def print(self, string):
        """
        Write the specified unicode string to the display.
        A newline ('\n') will advance to the left side of the next row.
        Lines that are too long automatically continue on next line.

        Only characters with an ``ord()`` value between 0 and 255 are currently
        supported.

        """
        for char in string:
            if char == '\n':
                # Advance to next row, at left side. Wrap around to top row if at bottom.
                self.set_cursor_pos((self._row + 1) % self.num_rows, 0)
            else:
                self.write(ord(char))


    def clear(self):
        """Overwrite display with blank characters and reset cursor position."""
        self.command(_LCD_CLEARDISPLAY)
        time.sleep(2*MILLISECOND)
        self.home()

    def home(self):
        """Set cursor to initial position and reset any shifting."""
        self.command(_LCD_RETURNHOME)
        self._row = 0
        self._col = 0
        time.sleep(2*MILLISECOND)

    def shift_display(self, amount):
        """Shift the display. Use negative amounts to shift left and positive
        amounts to shift right."""
        if amount == 0:
            return
        direction = _LCD_MOVERIGHT if amount > 0 else _LCD_MOVELEFT
        for i in range(abs(amount)):
            self.command(_LCD_CURSORSHIFT | _LCD_DISPLAYMOVE | direction)
            time.sleep(50*MICROSECOND)

    def create_char(self, location, bitmap):
        """Create a new character.

        The HD44780 supports up to 8 custom characters (location 0-7).

        :param location: The place in memory where the character is stored.
            Values need to be integers between 0 and 7.
        :type location: int
        :param bitmap: The bitmap containing the character. This should be a
            bytearray of 8 numbers, each representing a 5 pixel row.
        :type bitmap: bytearray
        :raises AssertionError: Raised when an invalid location is passed in or
            when bitmap has an incorrect size.

        Example:

        .. sourcecode:: python

            >>> smiley = bytearray(
            ...     0b00000,
            ...     0b01010,
            ...     0b01010,
            ...     0b00000,
            ...     0b10001,
            ...     0b10001,
            ...     0b01110,
            ...     0b00000,
            ... )
            >>> lcd.create_char(0, smiley)

        """
        if not (0 <= location <= 7):
            raise ValueError('Only locations 0-7 are valid.')
        if len(bitmap) != 8:
            raise ValueError('Bitmap should have exactly 8 rows.')

        # Store previous position
        save_row = self._row
        save_col = self._col

        # Write character to CGRAM
        self.command(_LCD_SETCGRAMADDR | location << 3)
        for row in bitmap:
            self.interface.send(row, _RS_DATA)

        # Restore cursor pos
        self.set_cursor_pos(save_row, save_col)

    def command(self, value):
        """Send a raw command to the LCD."""
        self.interface.send(value, _RS_INSTRUCTION)

    def write(self, value):
        """Write a raw character byte to the LCD."""
        self.interface.send(value, _RS_DATA)
        if self._col < self.num_cols - 1:
            # Char was placed on current line. No need to reposition cursor.
            self._col += 1
        else:
            # At end of line: go to left side next row. Wrap around to first row if on last row.
            self._row = (self._row + 1) % self.num_rows
            self._col = 0

        self.set_cursor_pos(self._row, self._col)

