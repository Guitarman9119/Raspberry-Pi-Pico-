import board
import time
import busio
import lcd
import i2c_pcf8574_interface
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



i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
address = 0x3F


i2c = i2c_pcf8574_interface.I2CPCF8574Interface(i2c, address)

display = lcd.LCD(i2c, num_rows=2, num_cols=16)

display.set_backlight(True)

display.set_display_enabled(True)

display.clear()
display.print("Welcome")

#---------------------------------------------------------------
# Run the main loop to generate a counting display.

btn1_pin = board.GP15
btn1 = digitalio.DigitalInOut(btn1_pin)
btn1.direction = digitalio.Direction.INPUT
btn1.pull = digitalio.Pull.DOWN

btn2_pin = board.GP14
btn2 = digitalio.DigitalInOut(btn2_pin)
btn2.direction = digitalio.Direction.INPUT
btn2.pull = digitalio.Pull.DOWN

btn3_pin = board.GP13
btn3 = digitalio.DigitalInOut(btn3_pin)
btn3.direction = digitalio.Direction.INPUT
btn3.pull = digitalio.Pull.DOWN

btn4_pin = board.GP12
btn4 = digitalio.DigitalInOut(btn4_pin)
btn4.direction = digitalio.Direction.INPUT
btn4.pull = digitalio.Pull.DOWN



while True:

    # Keycode class defines USB HID keycodes to send using Keyboard.  
    if btn1.value:
        display.clear()
        display.print("Open VLC")
        keyboard.send(Keycode.GUI)
        time.sleep(0.4)
        write_text.write('VLC\n')
        time.sleep(0.4)

        
        
    #The ConsumerControl class emulates consumer control devices such as remote controls, or the multimedia keys on certain keyboards.    
    if btn2.value:
        display.clear()
        display.print("Volume +")
        cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        time.sleep(0.1)

    #KeyboardLayoutUS class which allow us to send ASCII characters    
    if btn3.value:
        display.clear()
        display.print("Custom Text 1")
        write_text.write("Subscribe to NerdCave")
        time.sleep(0.1)

    #combination of different classes
    if btn4.value:
        display.clear()
        display.print("Select All")
        keyboard.send(Keycode.CONTROL, Keycode.A)
        time.sleep(0.1)

    
    time.sleep(0.1)

    