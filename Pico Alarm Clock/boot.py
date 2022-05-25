from machine import I2C, Pin
from ds1302 import DS1302
from pico_i2c_lcd import I2cLcd
import utime

buzzer = Pin(14, Pin.OUT)
buzzer.high()