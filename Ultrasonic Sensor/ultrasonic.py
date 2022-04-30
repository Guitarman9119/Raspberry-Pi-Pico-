from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import utime

WIDTH = 128
HEIGHT = 64

i2c = I2C(0, scl = Pin(17), sda = Pin(16), freq=400000)
display = SSD1306_I2C(WIDTH, HEIGHT, i2c)


trigger = Pin(21, Pin.OUT)
echo = Pin(20, Pin.IN)


def ultra():
   trigger.low()
   utime.sleep_us(2)
   trigger.high()
   utime.sleep_us(5)
   trigger.low()
   while echo.value() == 0:
       signaloff = utime.ticks_us()
   while echo.value() == 1:
       signalon = utime.ticks_us()
       
   timepassed = signalon - signaloff
   distance = (timepassed * 0.0343) / 2
   distance = "{:.1f}".format(distance)
   
   print(distance + " cm")
   
   return str(distance)



print("fok")
ngf = ultra()
print(ngf)
while True:
    display.text(ultra(),0,0)
    display.show()
    display.fill(0)
    utime.sleep(1)
    

    
    
    

    

  
    

