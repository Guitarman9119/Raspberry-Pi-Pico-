"""

DS1302 real-time clock module
Special thanks to yunline for the Library: https://github.com/omarbenhamid/micropython-ds1302-rtc
Remember to check out more tutorials on NerdCave - https://www.youtube.com/c/NerdCaveYT

Pinout
VCC - VSYS (PIN39)
GND - GND (Any ground on Pico)
CLK - GP18 (PIN24)
DAT - GP17 (PIN22)
RST  - GP16 (PIN21)

"""

import utime
import ds1302
from machine import I2C, Pin
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd


I2C_ADDR     = 63
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)



ds = ds1302.DS1302(Pin(18),Pin(17),Pin(16))

ds.date_time() # returns the current datetime.
ds.date_time([2023, 3, 2, 0, 8, 17, 50, 0]) # set datetime.

print(ds.date_time())


while True:
    
    lcd.clear()
    lcd.putstr(str(ds.year()) + "/" +  str(ds.month()) + "/" + str(ds.day()) + " " + str(ds.hour()) + ":" + str(ds.minute()) + ":" + str(ds.second()))
    utime.sleep(1)

    
    
'''
rtc=machine.RTC()
rtc.datetime((2020, 1, 21, 2, 10, 32, 36, 0))



while True:
    reading = sensor_temp.read_u16() * conversion_factor
    timestamp=rtc.datetime()
    temperature = 27 - (reading - 0.706)/0.001721

    timestring="%04d-%02d-%02d %02d:%02d:%02d"%(timestamp[0:3] +
                                                timestamp[4:7])
    print(timestring + "," + str(temperature) + "\n")

    led_onboard.value(1)
    utime.sleep(0.01)
    led_onboard.value(0)
'''

