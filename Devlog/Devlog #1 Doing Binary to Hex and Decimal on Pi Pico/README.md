#  Binary to Hexa / Decimal converter on Pi Pico

## Youtube Video Link
Please watch the video here and support the channel by pressing the like button and subsribing to the channel.


## Overview
This is the development video blog of the Binary to Hexa / decimal converter learning board, which I am working on.  Due to lockdown in Shanghai I am not able to receive the final PCB version yet, but it will be shared in this write up. The goal of this board is to teach you the fundamentals of number systems used in computers and serve as a great soldering practice board.

In terms of the Raspberry Pi Pico - You will learn how to connect the 16X2 Character LCD, setting up pins as inputs for the buttons and output for the LEDs, and learning MicroPython, related to the Pico.

Make sure to read the disclaimer at the bottom.

## Project description

The learning board will convert an 8-bit binary number to Decimal or Hexadecimal.

The board has 11 inputs, which include 8 buttons to select from bit 0 - 7, an add, subtract and reset button.
This will allow you set the bit high or low in an 8 bit number which will indicate through the LED - by turning LED on for 1 / High and off for a 0 / Low.

The Pico will take the 8 bit number and convert it into decimal and hexadecimal.

The 16x2 character LCD display will be used as output to indicate the results.
The LED will display the decimal, hexadecimal and binary number.

## Components needed

To follow along with this project you will need the following components:

- Raspberry Pi Pico
- 16 x 2 Character LCD display
- 11 Tactile push buttons
- 8 LED's
- 8 - 330 Ohm resistors
- Lot of wires and breadboard
- and finally patience



# Circuit Diagram 

To following along with the devlog circuit I have included the schematic diagram.

![My Image](images/schematic.png)

## PCB Design
I decided to make 3 seperate PCB files. Which is available in the repository.
- PCB 1 - with I2C LCD support, 8 Through hole LEDs
- PCB 2 - without I2C using 4 data pins, 8 Through hole LEDs
- PCB 3 - with I2C LCD support and 4 data pins, WS2812b LEDs

![My Image](images/PCB3D.png)
![My Image](images/PCB2D.png)



## Code Explanation

To code this project is straight forward. We will setup the pins to have 8 outputs for the LEDs and 11 inputs for the buttons.

### Libraries
Libraries needed: https://github.com/T-622/RPI-PICO-I2C-LCD

We start of by importing all the neccecary libraries.

    from machine import I2C, Pin
    import utime
    from lcd_api import LcdApi
    from pico_i2c_lcd import I2cLcd

To setup the I2C we need to know the I2C address. To get the address of your I2C LCD run the following script with LCD connected.

    import machine
    sda = machine.Pin(0)
    scl = machine.Pin(1)
    i2c = machine.I2C(0,sda=sda,scl=scl, freq=400000)
    print(i2c.scan())
    
This will give your I2C Address
Now we can setup the I2C 16x2 character display:

    I2C_ADDR     = 63
    I2C_NUM_ROWS = 2
    I2C_NUM_COLS = 16
    i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
    lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

The next step we will create a list of GP pins our LEDs will be connected to.
    
    LED_pins = [9,8,7,6,5,4,3,2]

Create an empty lists to set up and initialize pins as output by looping through the LED_pins list.

    LED = []
    for x in range(0,8):
        LED.append(Pin(LED_pins[x], Pin.OUT))
        LED[x].value(0)

We will repeat the same process for the buttons

    Button_pins = [17,16,15,14,13,12,11,10,18,19,20]
    Button = []
    # Loop to assign GPIO pins and setup input and outputs
    for x in range(0,11):
        Button.append(Pin(Button_pins[x], Pin.IN, Pin.PULL_DOWN))
        Button[x].value(0)

We will then create a counter that will allow us to store the denary value of the active bits that is High using the Decimal to Binary conversion table.

    counter = 0
    #Decimal to Binary conversion table 
    table = [1,2,4,8,16,32,64,128]

Before looking at the function written to control LED's and display the converter values, we first will look at the main loop.

We will first loop through the 8 buttons to see if any button is pushed. The buttons is connected to the 3.3V output of the Pico and using the internal pull-down resistors of the Pico to keep the pin low. When a button is pressed the value will go to 1.

We will first check if the LED value is 1 and button 1, which means the bit was already set, which we will then set the button value to zero, remove that bit decimal value from the table to counter. We print out the counter, and after a short delay we call the function display(), which we pass the value of counter.

If the LED was zero along with the button we will add the bit decimal value from the table to counter, print the counter value, followed by a short delay and calling
the display() function passing it the value of counter.

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

We then check the other 3 inputs which will be our Reset button to set our counter to zero and call the display() function, the other two buttons will add 1 to the counter or substract 1 from the counter. This will allow you to add one to counter between the value of 0 to 255.


    #Reset Button
            if Button[8].value() == 1:
                utime.sleep(0.1)
                counter = 0
                print(counter)
                utime.sleep(0.3)
                display(counter)
            
    #Add
            if Button[9].value() == 1:
                utime.sleep(0.1)
                counter += 1
                utime.sleep(0.3)
                display(counter)

    #Subtract
            if Button[10].value() == 1 and counter > -1:
                utime.sleep(0.1)
                counter -= 1
                utime.sleep(0.3)
                display(counter)


The main function display, will control the LCD and what we display to the LCD. We create an 8 bit binary digit from the counter and store it in a list LED_ON_OFF. We map this list to a string to be used to display to LCD. We then convert the counter to a hexadecimal value and then we can loop through the LED_ON_OFF list to set the LEDs High or Low depending on the counter value.

Then using the LCD library methods we write all the information to the LCD screen.

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
        utime.sleep(0.1)





## Disclaimer

The project code / schematic / tutorials etc. in this repository and youtube videos is provided “as is”, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall i be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the project.

