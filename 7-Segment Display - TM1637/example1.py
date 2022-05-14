import tm1637
from machine import Pin
from utime import sleep
mydisplay = tm1637.TM1637(clk=Pin(0), dio=Pin(1))

while True:
    
    # Show a word
    mydisplay.show("COOL")
    sleep(1)
     
    #blank the screen
    mydisplay.show("    ")
    sleep(1)
     
    #show numbers
    mydisplay.number(-502)
    sleep(4)

    mydisplay.show("    ")
    sleep(1)

    mydisplay.number(-418)
    sleep(4)

    #show scrolling text
    mydisplay.scroll("PICO IS COOL")
    sleep(1)
     
     
    #show temperature
    mydisplay.temperature(34)
    sleep(1)
     

    # Show a word
    mydisplay.show("COOL")
    sleep(1)
     
    #adjust the brightness to make it loewr
    for x in range(8):
        mydisplay.brightness(x)
        print(x)
        sleep(1)
 
