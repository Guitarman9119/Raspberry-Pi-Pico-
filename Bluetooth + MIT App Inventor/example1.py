from machine import Pin,UART #importing PIN and PWM
import utime #importing time


#Defining UART channel and Baud Rate
uart = UART(0,9600)


LED = Pin(14, Pin.OUT)



while True:
    
    
    if uart.any(): #Checking if data available
        data=uart.read() #Getting data
        data=str(data) #Converting bytes to str type
        print(data)
        
        if('LED_ON' in data):
            LED.value(1)
           
        elif('LED_OFF' in data):
            LED.value(0)
        
        
    
