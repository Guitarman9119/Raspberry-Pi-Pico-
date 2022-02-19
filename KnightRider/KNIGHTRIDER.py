# Knight Rider LED
from machine import Pin
import utime

#LED Pins to be used
LEDs = [16,17,18,19,20,21,22,26,27,28]

#create an empty list to assing pins in pico
led_pins = []

for x in range(0,10):
    led_pins.append(Pin(LEDs[x], Pin.OUT, Pin.PULL_UP))
    
button_fast = Pin(11,Pin.IN, Pin.PULL_DOWN)
button_slow = Pin(13,Pin.IN, Pin.PULL_DOWN)



delay = 0.002






def check_delay():
    global delay
    if button_fast.value():
        delay = max(0,delay - 0.001)
        utime.sleep(0.2)      
    if button_slow.value():
        delay = delay + 0.001
        utime.sleep(0.2)
    utime.sleep(delay)
        


                      

    

    
    
while True:
    
  ############ Left to Right ##################  
    for x in range(len(led_pins)-2):
        
        led_pins[x+1].value(1)
        check_delay()
        led_pins[x].value(1)
        check_delay()
        led_pins[x+1].value(1)
        check_delay()
        led_pins[x+2].value(1)
        check_delay()
        led_pins[x].value(0)
        check_delay()
        led_pins[x+1].value(1)
        check_delay()
        led_pins[x+2].value(0)
        

        
  ############ Left to Right ##################  
    for x in reversed(range(len(led_pins)-2)):
        
        led_pins[x+1].value(1)
        check_delay()
        led_pins[x].value(1)
        check_delay()
        led_pins[x+1].value(1)
        check_delay()
        led_pins[x+2].value(1)
        check_delay()
        led_pins[x].value(0)
        check_delay()
        led_pins[x+1].value(1)
        check_delay()
        led_pins[x+2].value(0)
       