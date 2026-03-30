import machine
import time


class LCD:
    def __init__(self, i2c, addr=None, cols=16, rows=2, blen=1):
        self.bus = i2c
        self.addr = self._scan_address(addr)
        self.cols = cols
        self.rows = rows
        self.blen = blen

        # Row offsets for different LCD sizes
        if rows == 1:
            self.row_offsets = [0x00]
        elif rows == 2:
            self.row_offsets = [0x00, 0x40]
        elif rows == 4:
            self.row_offsets = [0x00, 0x40, 0x14, 0x54]
        else:
            raise ValueError("Unsupported LCD size")

        self._init_lcd()

    # --------------------------
    # Initialization
    # --------------------------
    def _init_lcd(self):
        self.send_command(0x33)
        time.sleep(0.005)
        self.send_command(0x32)
        time.sleep(0.005)
        self.send_command(0x28)  # 4-bit, 2 line
        time.sleep(0.005)
        self.send_command(0x0C)  # Display ON, cursor OFF
        time.sleep(0.005)
        self.clear()

        self.openlight()

    def _scan_address(self, addr):
        devices = self.bus.scan()
        if not devices:
            raise Exception("No I2C devices found")

        if addr is not None:
            if addr in devices:
                return addr
            raise Exception(f"LCD at 0x{addr:02X} not found")

        for default in (0x27, 0x3F):
            if default in devices:
                return default

        return devices[0]

    # --------------------------
    # Low-level I2C
    # --------------------------
    def _write_word(self, data):
        if self.blen:
            data |= 0x08
        else:
            data &= 0xF7
        self.bus.writeto(self.addr, bytearray([data]))

    def _write_byte(self, data, mode):
        high = data & 0xF0
        low = (data & 0x0F) << 4

        self._write_4bits(high | mode)
        self._write_4bits(low | mode)

    def _write_4bits(self, data):
        self._write_word(data | 0x04)  # EN = 1
        time.sleep(0.0005)
        self._write_word(data & ~0x04)  # EN = 0
        time.sleep(0.0001)

    def send_command(self, cmd):
        self._write_byte(cmd, 0x00)

    def send_data(self, data):
        self._write_byte(data, 0x01)

    # --------------------------
    # High-level functions
    # --------------------------
    def clear(self):
        self.send_command(0x01)
        time.sleep(0.002)

    def home(self):
        self.send_command(0x02)
        time.sleep(0.002)

    def openlight(self):
        self._write_word(0x08)

    def backlight(self, state=True):
        self.blen = 1 if state else 0
        self._write_word(0x00)

    def set_cursor(self, col, row):
        if row >= self.rows:
            row = self.rows - 1
        if col >= self.cols:
            col = self.cols - 1

        addr = 0x80 + self.row_offsets[row] + col
        self.send_command(addr)

    def write(self, col, row, text):
        self.set_cursor(col, row)
        for char in text:
            self.send_data(ord(char))

    def message(self, text):
        row = 0
        col = 0

        for char in text:
            if char == "\n":
                row += 1
                col = 0
                if row >= self.rows:
                    break
                self.set_cursor(col, row)
            else:
                if col >= self.cols:
                    continue
                self.send_data(ord(char))
                col += 1
                