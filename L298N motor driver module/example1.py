from machine import Pin
import time #importing time for delay  


# Defining motor pins

#OUT1  and OUT2
In1=Pin(6,Pin.OUT) 
In2=Pin(7,Pin.OUT)  
EN_A=Pin(8,Pin.OUT)



#OUT3  and OUT4
In3=Pin(4,Pin.OUT)  
In4=Pin(3,Pin.OUT)  
EN_B=Pin(2,Pin.OUT)

EN_A.high()
EN_B.high()
# Forward
def move_forward():
    In1.high()
    In2.low()
    In3.high()
    In4.low()
    
# Backward
def move_backward():
    In1.low()
    In2.high()
    In3.low()
    In4.high()
    
#Turn Right
def turn_right():
    In1.low()
    In2.low()
    In3.low()
    In4.high()
    
#Turn Left
def turn_left():
    In1.low()
    In2.high()
    In3.low()
    In4.low()
   
#Stop
def stop():
    In1.low()
    In2.low()
    In3.low()
    In4.low()
    
while True:
    move_forward()
    print("Forward")
    time.sleep(2)
    stop()
    print("Stop")
    time.sleep(2)
    move_backward()
    print("Backward")   
    time.sleep(2)
    stop()
    print("Stop")
    time.sleep(2)