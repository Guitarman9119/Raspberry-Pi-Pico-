'''Simple Program to Find I2C in CircuitPython adapted from:
https://learn.adafruit.com/scanning-i2c-addresses/circuitpython'''

import time
import board
import busio

i2c = busio.I2C(board.GP1, board.GP0)    # Pi Pico RP2040

while not i2c.try_lock():
    pass

try:
    while True:
        print(
            "I2C addresses found:",
            [hex(device_address) for device_address in i2c.scan()],
        )
        time.sleep(2)

finally: 
    i2c.unlock()