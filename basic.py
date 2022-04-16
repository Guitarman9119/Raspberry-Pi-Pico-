from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf
import time


i2c = I2C(0, scl = Pin(17), sda = Pin(16), freq=400000)

display = SSD1306_I2C(128, 64, i2c)




    

    

  
    


