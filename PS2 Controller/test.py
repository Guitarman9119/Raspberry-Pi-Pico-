from machine import I2C, Pin
from ps2 import PS2Controller
import utime


ps2ctl = PS2Controller(di_pin_no=7, do_pin_no=8, cs_pin_no=9, clk_pin_no=10)

while True:
    utime.sleep(0.2)
    
    read = ps2ctl.run()
    print(read)
    utime.sleep(0.2)