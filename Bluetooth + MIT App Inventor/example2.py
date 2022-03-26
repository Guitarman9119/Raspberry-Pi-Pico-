from machine import Pin,UART #importing PIN and PWM
import utime #importing time

#Defining UART channel and Baud Rate
uart= UART(0,9600)

#Create a list of all the LED pins
leds = [9,10,11,12,13,14]

#Assign LED's in list as an Output
led_pins = [Pin(pin_name, mode=Pin.OUT) for pin_name in leds]

#Setup Pin18 to control Relay
Relay = Pin(18, Pin.OUT)


#Functions for patterns
def pattern1():
    delay = 0.02
    count = 0
    while(count<2):
        
    
        for x in range(len(led_pins)):
            led_pins[x].value(1)
            utime.sleep(delay)
            led_pins[x].value(0)
            utime.sleep(delay)
        for x in reversed(range(len(led_pins))):
            led_pins[x].value(1)
            utime.sleep(delay)
            led_pins[x].value(0)
            utime.sleep(delay)
            
        count = count + 1

#Pattern 2
def pattern2():
    x = 0
    while(x<2):
        
        wait = 0.5
   
        led_pins[0].value(1)
        led_pins[5].value(1)
        utime.sleep(wait)
        
        led_pins[0].value(0)
        led_pins[5].value(0)
       
        led_pins[1].value(1)
        led_pins[4].value(1)
        utime.sleep(wait)
        
        led_pins[1].value(0)
        led_pins[4].value(0)
    
        led_pins[2].value(1)
        led_pins[3].value(1)
        utime.sleep(wait)
        
        led_pins[2].value(0)
        led_pins[3].value(0)
        
        x = x + 1
        



#Pattern 3
def pattern3():
    x = 0
    while(x<2):
        
        wait = 0.5
   
        led_pins[2].value(1)
        led_pins[3].value(1)
        utime.sleep(wait)
        
        led_pins[2].value(0)
        led_pins[3].value(0)
       
        led_pins[1].value(1)
        led_pins[4].value(1)
        utime.sleep(wait)
        
        led_pins[1].value(0)
        led_pins[4].value(0)
    
        led_pins[0].value(1)
        led_pins[5].value(1)
        utime.sleep(wait)
        
        led_pins[0].value(0)
        led_pins[5].value(0)
        
        x = x + 1       

while True:
    
    if uart.any(): #Checking if data available
        data=uart.read() #Getting data
        data=str(data) #Converting bytes to str type
        print(data)
        
        if('LED1_ON' in data):
            led_pins[0].value(1)
           
        elif('LED1_OFF' in data):
            led_pins[0].value(0)
        
        if('LED2_ON' in data):
            led_pins[1].value(1)
         
        elif('LED2_OFF' in data):
            led_pins[1].value(0)        
        
        if('LED3_ON' in data):
            led_pins[2].value(1)
        
        elif('LED3_OFF' in data):
            led_pins[2].value(0)        
        
        if('LED4_ON' in data):
            led_pins[3].value(1)
          
        elif('LED4_OFF' in data):
            led_pins[3].value(0)        
        
        if('LED5_ON' in data):
            led_pins[4].value(1)
           
        elif('LED5_OFF' in data):
            led_pins[4].value(0)               
       
        if('LED6_ON' in data):
            led_pins[5].value(1)
            
        elif('LED6_OFF' in data):
            led_pins[5].value(0)        
        
        if("pattern_1" in data):
            pattern1()
          
        if("pattern_2" in data):
            pattern2()
            
        if("pattern_3" in data):
            pattern3()           
        
        if("Relay_on" in data):
            Relay.value(1)
            
        elif("Relay_off" in data):
            Relay.value(0)
    
    