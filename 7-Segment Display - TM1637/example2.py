import tm1637
from machine import I2C, Pin
from utime import sleep
import ds1302
mydisplay = tm1637.TM1637(clk=Pin(0), dio=Pin(1))
ds = ds1302.DS1302(Pin(18),Pin(17),Pin(16))

ds.date_time([2023, 3, 2, 0, 8, 17, 50]) # set datetime.
 


while True:

    (Y,M,D,day,hr,m,s)=ds.date_time()


    mydisplay.numbers(hr,m)
    sleep(1)
