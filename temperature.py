from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf
import time

WIDTH = 128
HEIGHT = 64

i2c = I2C(0, scl = Pin(17), sda = Pin(16), freq=400000)

display = SSD1306_I2C(128, 64, i2c)

# display.invert(1)
#display.contrast(100)

def read_temp():
    sensor_temp = machine.ADC(4)
    conversion_factor = 3.3 / (65535)
    reading = sensor_temp.read_u16() * conversion_factor 
    temperature = 27 - (reading - 0.706)/0.001721
    formatted_temperature = "{:.1f}".format(temperature)
    string_temperature = str("Temperature:" + formatted_temperature)
    print(string_temperature)
    time.sleep(2)
    return string_temperature


while True:
    display.text('Example 1:',0,0)
    temperature = read_temp()
    display.text(temperature,0,14)
    display.show()
    display.fill(0)
    
    
    

    

  
    

