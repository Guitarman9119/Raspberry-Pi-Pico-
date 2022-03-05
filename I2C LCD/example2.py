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

#ds = ds1302.DS1302(Pin(2),Pin(3),Pin(4))

#ds.date_time() # returns the current datetime.
#ds.date_time([2023, 3, 2, 0, 8, 17, 0, 0]) # set datetime.

#ds.hour() # returns hour.
#print(ds.date_time())





def read_temp():
    sensor_temp = machine.ADC(4)
    conversion_factor = 3.3 / (65535)
    reading = sensor_temp.read_u16() * conversion_factor 
    temperature = 27 - (reading - 0.706)/0.001721
    formatted_temperature = "{:.2f}".format(temperature)
    string_temperature = str("Temp:" + formatted_temperature)
    print(string_temperature)
    utime.sleep(2)
    return string_temperature



while True:
   
    temperature = read_temp()
    lcd.move_to(0,0)
    lcd.putstr(temperature)


   
   
   
   
   
   # time = utime.localtime()
    #lcd.putstr(str(ds.year()) + "/" +  str(ds.month()) + "/" + str(ds.day()) + " " + str(ds.hour()) + ":" + str(ds.minute()))
    


