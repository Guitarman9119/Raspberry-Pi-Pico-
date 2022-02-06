# Matrix Keypad
# NerdCave - https://www.youtube.com/channel/UCxxs1zIA4cDEBZAHIJ80NVg

from machine import Pin
import utime


# Create a map between keypad buttons and characters

matrix_keys = [['1', '2', '3', 'A'],
               ['4', '5', '6', 'B'],
               ['7', '8', '9', 'C'],
               ['*', '0', '#', 'D']]

# Define PINs according to cabling
keypad_rows = [9,8,7,6]
keypad_columns = [5,4,3,2]


col_pins = []
row_pins = []

## the keys entered by the user
guess = []
#our secret pin, shhh do not tell anyone
secret_pin = ['1','2','3','4','5','6']
#setup pin to be an output
led = Pin(15, Pin.OUT, Pin.PULL_UP)

for x in range(0,4):
    row_pins.append(Pin(keypad_rows[x], Pin.OUT))
    row_pins[x].value(1)
    col_pins.append(Pin(keypad_columns[x], Pin.IN, Pin.PULL_DOWN))
    col_pins[x].value(0)
    
##############################Scan keys ####################
    
def scankeys():
    
    for row in range(4):
        for col in range(4): 
            row_pins[row].high()
            key = None
            
            if col_pins[col].value() == 1:
                print("You have pressed:", matrix_keys[row][col])
                key_press = matrix_keys[row][col]
                utime.sleep(0.3)
                guess.append(key_press)
               
                
            if len(guess) == 6:
                checkPin(guess)
                
                for x in range(0,6):
                    guess.pop() 
                    
        row_pins[row].low()
    

##############################To check Pin #################
def checkPin(guess):
             
    if guess == secret_pin:
        
        print("You got the secret pin correct")
        led.value(1)
        utime.sleep(3)
        led.value(0)
        
    else:
        print("Better luck next time")     
        
            
    
        
        
  
    
    
    

###########################################################
    
print("Enter the secret Pin")


while True:
    
    scankeys()
    
   
            

           
