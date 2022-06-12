from machine import Pin,PWM,UART #importing PIN and PWM
import time #importing time

#Defining UART channel and Baud Rate
uart= UART(0,9600)

#OUT1  and OUT2
In1=Pin(6,Pin.OUT)  #IN1`
In2=Pin(7,Pin.OUT)  #IN2


#OUT3  and OUT4
In3=Pin(4,Pin.OUT)  #IN3
In4=Pin(3,Pin.OUT)  #IN4


EN_A=PWM(Pin(8))
EN_B=PWM(Pin(2))
# Defining frequency for enable pins
EN_A.freq(1500)
EN_B.freq(1500)

# Setting maximum duty cycle for maximum speed (0 to 65025)
EN_A.duty_u16(65025)
EN_B.duty_u16(65025)

# Left
def turn_left():
    In1.high()
    In2.low()
    In3.low()
    In4.high()
    
# Right
def turn_right():
    In1.low()
    In2.high()
    In3.high()
    In4.low()
    
# Backward
def move_backward():
    In1.low()
    In2.high()
    In3.low()
    In4.high()
    
# Forward
def move_forward():
    In1.high()
    In2.low()
    In3.high()
    In4.low()
    
# Stop
def stop():
    In1.low()
    In2.low()
    In3.low()
    In4.low()

while True:
    if uart.any(): #Checking if data available
        data=uart.read() #Getting data
        data=str(data) #Converting bytes to str type
        print(data)
        if('forward' in data):
            move_forward() #Forward
        elif('backward' in data):
            move_backward() #Backward
        elif('right' in data):
            turn_right() #Turn Right
        elif('left' in data):
            turn_left() #Turn Left
        elif('stop' in data):
            stop() #Stop
        elif('E' in data):
            speed=data.split("|")
            print(speed[1])
            set_speed = float(speed[1])/100 * 65025
            EN_A.duty_u16(int(set_speed)) #Setting Duty Cycle
            EN_B.duty_u16(int(set_speed)) #Setting Duty Cycle
        else:
            stop() #Stop
    