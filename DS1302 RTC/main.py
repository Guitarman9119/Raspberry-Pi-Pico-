"""

DS1302 real-time clock module

Special thanks to yunline for the DS1302  Library: https://github.com/omarbenhamid/micropython-ds1302-rtc
and T-622 for the I2C LCD library: https://github.com/T-622/RPI-PICO-I2C-LCD

Remember to check out more tutorials on NerdCave - https://www.youtube.com/c/NerdCaveYT

Project Pinout
VCC - VSYS (PIN39)
GND - GND (Any ground on Pico)
CLK - GP18 (PIN24)
DAT - GP17 (PIN22)
RST  - GP16 (PIN21)

"""


from machine import I2C, Pin
from ds1302 import DS1302
from pico_i2c_lcd import I2cLcd

I2C_ADDR     = 63
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

ds = DS1302(Pin(18),Pin(17),Pin(16))

ds.date_time() # returns the current datetime.

#ds.date_time([2023, 3, 2, 0, 8, 17, 50, 0]) # set datetime.

#ds.hour() # returns hour.
#print(ds.date_time())


while True:
    (Y,M,D,day,hr,m,s)=ds.date_time()
    if s < 10:
        s = "0" + str(s)
    if m < 10:
        m = "0" + str(m)
    if hr < 10:
        hr = "0" + str(hr)
    if D < 10:
        D = "0" + str(D)
    if M < 10:
        M = "0" + str(M)
        
    lcd.move_to(0,0)
    lcd.putstr("Time:")
    lcd.move_to(6,0)
    lcd.putstr(str(hr) + ":" + str(m) + ":" + str(s))
    lcd.move_to(0,1)
    lcd.putstr("Date:")
    lcd.move_to(6,1)
    lcd.putstr(str(D) + "/" + str(M) + "/" + str(Y))
   
