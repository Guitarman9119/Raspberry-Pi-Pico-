from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf
import time

WIDTH = 128
HEIGHT = 64

i2c = I2C(0, scl = Pin(17), sda = Pin(16), freq=400000)
display = SSD1306_I2C(WIDTH, HEIGHT, i2c)


images = []
for n in range(1, x):
    with open('/folder/image%s.pbm' % n, 'rb') as f:  #open folder and image
        f.readline() # Magic number
        f.readline() # Creator comment
        f.readline() # Dimensions
        data = bytearray(f.read())
    fbuf = framebuf.FrameBuffer(data, 64, 64, framebuf.MONO_HLSB) #adjust accordingly the width and height
    images.append(fbuf)
    


while True:
    for i in images:
        display.blit(i, 32, 0)
        display.show()
        time.sleep(0.01)

