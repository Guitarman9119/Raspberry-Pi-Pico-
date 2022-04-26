from machine import Pin
import utime


DT_Pin = Pin(0, Pin.IN, Pin.PULL_UP)
CLK_Pin = Pin(1, Pin.IN, Pin.PULL_UP)
SW = Pin(2, Pin.IN, Pin.PULL_UP)

LEDs = [3,4,5,6,7,8]

#create an empty list to assing pins in pico
led_pins = []

for x in range(0,6):
    led_pins.append(Pin(LEDs[x], Pin.OUT))
    

value = 0
previousValue = 1


def rotary_changed():
    
    global previousValue
    global value
    
    if previousValue != CLK_Pin.value():
        if CLK_Pin.value() == 0:
            if DT_Pin.value() == 0:
          
                value = (value - 1)%6
                print("anti-clockwise", value)
            else:
        
                
                value = (value + 1)%6
                print("clockwise", value)                
        previousValue = CLK_Pin.value()
         
         
    if SW.value() == 0:       
        print("Button pressed")
        utime.sleep(1) 

    


while True:
    for i in range(0,6):
        led_pins[i].value(0)
        rotary_changed()
        led_pins[value].value(1)
        utime.sleep(0.001)            
    
