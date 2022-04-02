
'''

This is a pico macro keyboard based on CircuitPython adafruit_hid library
The PCB is currently in version one and thus the key layout is all crazy
like this:

    ****This will be fixed in Final version***

         key[0]    Key[3]   Key[6]

         key[1]    Key[4]   Key[7]

         key[2]    Key[5]   Key[8]

         key[9]    Key[10]   Key[11]

'''
#Import all the relevant Libraries

import time
import board
import digitalio
import usb_hid
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# Set up Consumer Control - Control Codes can be found here: https://docs.circuitpython.org/projects/hid/en/latest/_modules/adafruit_hid/consumer_control_code.html#ConsumerControlCode
cc = ConsumerControl(usb_hid.devices)

# Set up a keyboard device. - Keycode can be found here: https://docs.circuitpython.org/projects/hid/en/latest/_modules/adafruit_hid/keycode.html#Keycode
keyboard = Keyboard(usb_hid.devices)

# Set up keyboard to write strings from macro
write_text = KeyboardLayoutUS(keyboard)

# These are the corresponding GPIOs on the Pi Pico that is used for the Keys on the PCB
buttons = [board.GP0, board.GP1,board.GP2,board.GP3,board.GP4,board.GP5,board.GP6,board.GP7,board.GP8,board.GP9,board.GP10,board.GP11]
key = [digitalio.DigitalInOut(pin_name) for pin_name in buttons]
for x in range(0,len(buttons)):
    key[x].direction = digitalio.Direction.INPUT
    key[x].pull = digitalio.Pull.DOWN



while True:
    
    if key[0].value:
        cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        time.sleep(0.1)
        
    if key[1].value:
        cc.send(ConsumerControlCode.PLAY_PAUSE)
        time.sleep(0.1)
        
    if key[2].value:
        keyboard.send(Keycode.GUI)
        time.sleep(0.3)
        write_text.write('Brave\n')
        time.sleep(1)
        write_text.write('https://www.youtube.com/watch?v=l7SwiFWOQqM\n')
        
    if key[3].value:
        cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        time.sleep(0.1)
        
    if key[4].value:
        print("test")
        keyboard.send(Keycode.N)
        time.sleep(0.1)
        
    if key[5].value:
        keyboard.send(Keycode.GUI)
        time.sleep(0.3)
        write_text.write('Thonny\n')
        
    if key[6].value:
        cc.send(ConsumerControlCode.MUTE)
        time.sleep(0.1)
        
    if key[7].value:
        keyboard.send(Keycode.P)
        time.sleep(0.1)
        
    if key[8].value:
        write_text.write("I am text from the Pico Macro Keyboard")
        time.sleep(0.1)
        
    if key[9].value:
        keyboard.send(Keycode.ONE)
        time.sleep(0.1)
        
    if key[10].value:
        keyboard.send(Keycode.GUI)
        time.sleep(0.3)
        write_text.write('Brave\n')
        time.sleep(1)
        write_text.write('https://www.youtube.com/channel/UCxxs1zIA4cDEBZAHIJ80NVg\n')
        
    if key[11].value:
        keyboard.send(Keycode.THREE)
        time.sleep(0.1)

    time.sleep(0.1)