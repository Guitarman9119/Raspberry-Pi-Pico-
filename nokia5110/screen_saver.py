# pcd8544_fb (Nokia 5110) LCD sample for Raspberry Pi Pico
# https://github.com/mcauser/micropython-pcd8544/tree/791d4239d77b0d06192c7ab7903d81a72a53f992/examples
# Connections:
#   Connect the screen up as shown below using the
#   physical pins indicated (physical pin on pico)

#   RST - Reset:                     Pico GP8 (11)     #
#   CE - Chip Enable / Chip select : Pico GP5 ( 7)     #
#   DC - Data/Command :              Pico GP4 ( 6)     #
#   Din - Serial Input (Mosi):       Pico GP7 (10)
#   Clk - SPI Clock:                 Pico GP6 ( 9)
#   Vcc:                             Pico 3V3 (36)
#   BL :                             Pico GP9(12)
#   Gnd:                             Pico GND (38)


import pcd8544_fb
import math
from machine import Pin, SPI
import utime


spi = SPI(0)
spi.init(baudrate=2000000, polarity=0, phase=0)
cs = Pin(5)
dc = Pin(4)
rst = Pin(8)

# set bl on/off
bl = Pin(9, Pin.OUT, value=1)

#initialize lcd
lcd = pcd8544_fb.PCD8544_FB(spi, cs, dc, rst)

import framebuf
buffer = bytearray((pcd8544_fb.HEIGHT // 8) * pcd8544_fb.WIDTH)
fbuf = framebuf.FrameBuffer(buffer, pcd8544_fb.WIDTH, pcd8544_fb.HEIGHT, framebuf.MONO_VLSB)

# smiley 15x15 - col major msb
smiley = bytearray(b'\xE0\x38\xE4\x22\xA2\xE1\xE1\x61\xE1\x21\xA2\xE2\xE4\x38\xE0\x03\x0C\x10\x21\x21\x41\x48\x48\x48\x49\x25\x21\x10\x0C\x03')
smiley_w = 15
smiley_h = 15
smiley_fbuf = framebuf.FrameBuffer(smiley, smiley_w, smiley_h, framebuf.MONO_VLSB)

# area the smiley can move in
bounds_w = pcd8544_fb.WIDTH - smiley_w
bounds_h = pcd8544_fb.HEIGHT - smiley_h

# direction smiley is moving
move_x = 1
move_y = 1

# pause between displaying frames
from time import sleep_ms
pause = 100

# start position
x = 1
y = 1

def render():
    global x
    global y
    global move_x
    global move_y
    # Draw the bitmap
    fbuf.fill(0)
    fbuf.blit(smiley_fbuf, x, y, 0)
    lcd.data(buffer)

    sleep_ms(pause)

    # Move down right until hit bounds
    # Then flip increment to decrement to bounce off the wall
    x = x + move_x
    y = y + move_y
    if (x <= 0 or x >= bounds_w):
        move_x = -move_x
    if (y <= 0 or y >= bounds_h):
        move_y = -move_y

while(True):
    render()
