import utime
from machine import I2C, Pin
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

I2C_ADDR     = 63
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

LED_pins = [9,8,7,6,5,4,3,2]
#LED_pins = [2,3,4,5,6,7,8,9]

# Create two empty lists to set up pins ( Rows output and columns input )
LED = []



# Loop to assign GPIO pins and setup input and outputs
for x in range(0,8):

    LED.append(Pin(LED_pins[x], Pin.OUT))
    LED[x].value(0)


Button_pins = [17,16,15,14,13,12,11,10,18,19,20]

Button = []
# Loop to assign GPIO pins and setup input and outputs
for x in range(0,11):

    Button.append(Pin(Button_pins[x], Pin.IN, Pin.PULL_DOWN))
    Button[x].value(0)
    
counter = 0
#Decimal to Binary conversion table 
table = [1,2,4,8,16,32,64,128]
loop = 0


def counter_func():
    global loop
    global counter
          

        
    for x in range(0,255):
        counter += 1
        utime.sleep(0.5)
        display(counter)
        loop += x 
            


def display(counter):
    
    #create a binary value from the counter value passed to check which LED should be turned on or off
    LED_ON_OFF = [1 if counter & (1 << (7-n)) else 0 for n in range(8)]
    
    #map the list together to a string to display
    binary_display = ''.join(map(str,LED_ON_OFF))
    

    
    
    #reverse the order of the LED list
    LED_ON_OFF.reverse()
    
    #Loop through values in LED_ON_OFF list to set LEDs High or Low
    for i in range(8):
        LED[i].value(int(LED_ON_OFF[i])) 
     
    #string formatting
    #converter the counter to hexadecimal
    hexa = hex(counter).replace("0x", "")
    #hexa = hexa[2:]
    while len(hexa) < 2:
        hexa = '0' + hexa
    hexa = '0x' + hexa


    decimal = str(counter)
    while len(decimal) < 3:
        decimal = '0' + decimal
    
    
    lcd.move_to(0,0)
    lcd.putstr("Dec:")
    lcd.putstr(decimal)
    
    lcd.move_to(8,0)
    lcd.putstr("Hex:")
    lcd.putstr(str(hexa).upper())
    
    lcd.move_to(0,1)
    lcd.putstr("Bin:")
    lcd.putstr(binary_display)
    utime.sleep(0.01)
    
display(0)   
    
while True: 
    for x in range(0,8):
        if Button[x].value() == 1:
            utime.sleep(0.1)
            if LED[x].value() == 1 and Button[x].value() == 1:
                Button[x].value(0)
                counter = counter - table[x]
                print(counter)
                utime.sleep(0.3)
                display(counter)
                
            elif LED[x].value() == 0 and Button[x].value() == 0:
                counter = counter + table[x]
                print(counter)
                utime.sleep(0.3)
                display(counter)
        

                
                
                
#Counter
        if Button[8].value() == 1:
            utime.sleep(0.1)
            counter = 0
            print(counter)
            utime.sleep(0.3)
            display(counter)
            
#Add
        if Button[9].value() == 1 and counter < 255:
            utime.sleep(0.1)
            counter += 1
            utime.sleep(0.3)
            display(counter)

#Subtract
        if Button[10].value() == 1 and counter > 0: 
            utime.sleep(0.1)
            counter -= 1
            utime.sleep(0.3)
            display(counter)
            
# #Counter
#         if Button[8].value() == 1:
#                 counter = 0
#                 counter_func()
