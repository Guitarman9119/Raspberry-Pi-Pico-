from machine import Pin, PWM
import utime

flame_sensor = Pin(16, Pin.IN)
buzzer = Pin(17, Pin.OUT)
utime.sleep(0.5)

buzzer.high()

#OUT1  and OUT2
In1=Pin(1,Pin.OUT)  #IN1`
In2=Pin(0,Pin.OUT)  #IN2
EN_A=PWM(Pin(2))

# Defining frequency for enable pins
EN_A.freq(1500)

duty_cycle = 65535

while True:
    while flame_sensor.value() == 1:
        print("Flame Detected")
        
        buzzer.low()
        In1.low()
        In2.high()
        EN_A.duty_u16(int(duty_cycle/2))
    
    if flame_sensor.value() == 0:
                
        buzzer.high()
        In1.low()
        In2.low()
        print("No Flame")



utime.sleep(0.2)