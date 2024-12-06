
### YouTube Video
https://www.youtube.com/embed/buD-oxZESaU

## Introduction

Welcome to this tutorial on creating a Macro keyboard with a Joystick and a Custom PCB using EasyEDA and Raspberry Pi Pico with Circuit Python.

### What is a macro keyboard?

Macro keyboards are an excellent way to streamline your workflow and increase productivity. With a macro keyboard, you can automate repetitive tasks, execute complex commands with a single key press, and customize your keyboard layout to your needs. This version includes a working Joystick that could be used as a mouse.

### Component List

Here is the breakdown of components needed for the Macro Keyboard (assuming you have basic tools):

| Components          | Quantity            |
| ------------------- | ------------------- |
| Custom PCB          | 1                   |
| Raspberry Pi Pico   | 1                   |
| Mechanical Switches | 12                  |
| 1.3 OLED I2C        | 1                   |
| Rotary encoder      | 1                   |
| Resistors - 10k     | 3                   |
| 2.54 20 pin Header  | 2                   |



## Schematic Diagram

The schematic diagram is available to view here. The design is straightforward as each button was connected to a GPIO pin to the Raspberry Pi Pico. The reason for not using a matrix is due to limited space on a 10 x 10 cm board size, which meant individual GPIO pins could be used. This also means that diodes are not needed to prevent ghosting effect when pressing the keys. The board is kept this dimension to minimize the total cost of the board. Any other shape of Layout can be achieved to fully customize your keyboard but keep it smaller then 10 x 10 cm for the PCB reduced the cost of the project.


<figure><img src="images/schematic_macro_joystick.png" alt=""><figcaption></figcaption></figure>


## PCB Design

In this project, I've engineered a custom PCB (Printed Circuit Board) that simplifies the assembly process. The advantage of creating a unique PCB design allows us to skip the usual wiring process usually required. By customizing our PCB, we've inherently streamlined the assembly process to be quicker and more efficient.

### PCB Top:

<figure><img src="images/pcb_joystick_front.png" alt=""><figcaption></figcaption></figure>

### PCB Bottom:

<figure><img src="images/pcb_joystick_bottom.png" alt=""><figcaption></figcaption></figure>

### Order PCB (JLCPCB)

The PCB was ordered through JLCPCB. They offer great PCBs at a low cost and have promotions and coupons available throughout the year. You can sign up using here, or using the following link:

[https://jlcpcb.com/?from=Nerd](https://jlcpcb.com/?from=Nerd) that will support me as a creator to keep making content that is accessible and open source at no charge to you.

Ordering the PCB is very simple:

Download the Gerber file [here](https://github.com/Guitarman9119/Raspberry-Pi-Pico-/raw/main/Macro%20Keyboard%20Joystick/Macro_keyboard_joystick.zip).

Click on Add Gerber file

<figure><img src="images/pcbadd.png" alt=""><figcaption></figcaption></figure>

leave all the settings as default given. You might want change the PCB color which you can do here:

<figure><img src="images/22.png" alt=""><figcaption></figcaption></figure>

Enter you shipping details, save to cart

<figure><img src="images/33.png" alt=""><figcaption></figcaption></figure>

Then after a few days depending on your location you will receive your great quality PCB.



## Circuit Python

CircuitPython is a variant of the Python programming language designed for microcontrollers, specifically those based on the ARM Cortex-M family of processors. It allows developers to write Python code that can interact with hardware components and sensors, making it a popular choice for DIY electronics projects.

One advantage of using CircuitPython for building a macro keyboard is that it includes the HID (Human Interface Device) library, which allows microcontrollers to act as USB input devices such as keyboards, mice, and gamepads. This means that with CircuitPython, you can program your microcontroller to act like a keyboard and send keystrokes to your computer when a button is pressed on your macro keyboard.

Another advantage of CircuitPython is its ease of use and rapid prototyping capabilities. Since CircuitPython is an interpreted language, developers can write and test code on their computer before uploading it to the microcontroller. Additionally, CircuitPython comes with a large number of built-in libraries and modules that simplify programming for common hardware components, such as OLED displays, sensors, and LED strips. This can save a lot of time and effort compared to writing low-level code in C or assembly language.

### HID Library

In order to get the Raspberry Pi Pico to work as an macro keyboard we need to install a Human Interface Device Library from Adafruit Circuit Python library.

You need to create a folder on your Raspberry Pi Pico named "[adafruit\_hid](https://github.com/Guitarman9119/Raspberry-Pi-Pico-/tree/main/Pico%20Macro%20Keyboard/adafruit\_hid)" and upload the following files in the folder. You can download the files on my GitHub repository. It is also available on Circuit Python website but in order to keep version control for this specific tutorial along with the video I recommend you download it from my GitHub repository.







## Code

To follow along with this tutorial make sure you flash the Pico with CircuitPython 7.2.3 which you can download here:

CircuitPython - [v7.2.3](https://github.com/Guitarman9119/Raspberry-Pi-Pico-/tree/main/Macro%20Keyboard%20Joystick)

All the code can be downloaded here:

[Code](https://github.com/Guitarman9119/Raspberry-Pi-Pico-/tree/main/Macro%20Keyboard%20Joystick)

### code.py

This is the main file that will be booted once your power the Pico. Comments is given in the code as detailed as possible and explained below.

```python
import board, busio, displayio, os, terminalio
import adafruit_displayio_ssd1306
from adafruit_display_text import label
import usb_hid
import digitalio
import time
import rotaryio

"""CircuitPython Essentials HID Mouse example"""
import analogio
from adafruit_hid.mouse import Mouse

from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode


from blender_mode import handle_keypress as blender_mode_handle_keypress
from windows_mody import handle_keypress as windows_mode_handle_keypress
from premier_mode import handle_keypress as premier_mode_handle_keypress
from aftereffects_mode import handle_keypress as aftereffects_mode_handle_keypress
from fusion360_mode import handle_keypress as fusion360_mode_handle_keypress

#____________________________________________________________________________________
# Define constants
pot_min = 0.00
pot_max = 3.29
step = (pot_max - pot_min) / 20.0

# Setup mouse
mouse = Mouse(usb_hid.devices)
x_axis = analogio.AnalogIn(board.GP27)
y_axis = analogio.AnalogIn(board.GP26)
select = digitalio.DigitalInOut(board.GP20)
select.direction = digitalio.Direction.INPUT
select.pull = digitalio.Pull.UP

def get_voltage(pin):
    return (pin.value * 3.3) / 65536

def steps(axis):
    """ Maps the potentiometer voltage range to 0-20 """
    return round((axis - pot_min) / step)


# Set up Consumer Control - Control Codes can be found here: https://docs.circuitpython.org/projects/hid/en/latest/_modules/adafruit_hid/consumer_control_code.html#ConsumerControlCode
cc = ConsumerControl(usb_hid.devices)

# Set up a keyboard device. - Keycode can be found here: https://docs.circuitpython.org/projects/hid/en/latest/_modules/adafruit_hid/keycode.html#Keycode
keyboard = Keyboard(usb_hid.devices)

# Set up keyboard to write strings from macro
write_text = KeyboardLayoutUS(keyboard)

displayio.release_displays()

sda, scl = board.GP16, board.GP17  
i2c = busio.I2C(scl, sda)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
print(display_bus)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(128, 64, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(118, 54, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=5)
splash.append(inner_sprite)

# Draw a label
text = "NerdCave!"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=35, y=28)
splash.append(text_area)

# Draw a label
text2 = "MacroKeyboard"
text_area2 = label.Label(terminalio.FONT, text=text2, color=0xFFFF00, x=26, y=40)
splash.append(text_area2)

# These are the corresponding GPIOs on the Pi Pico that is used for the Keys on the PCB
buttons = [board.GP0,board.GP1,board.GP2,board.GP3,board.GP4,board.GP5,board.GP6,board.GP7,board.GP8,board.GP9,board.GP10]
key = [digitalio.DigitalInOut(pin_name) for pin_name in buttons]
for x in range(0,len(buttons)):
    key[x].direction = digitalio.Direction.INPUT
    key[x].pull = digitalio.Pull.DOWN

modeChangeButton = digitalio.DigitalInOut(board.GP11)
modeChangeButton.direction = digitalio.Direction.INPUT
modeChangeButton.pull = digitalio.Pull.DOWN

#___________________Setup Rotary Encoder____________________________
DT_Pin1 = digitalio.DigitalInOut(board.GP12)
DT_Pin1.direction = digitalio.Direction.INPUT
DT_Pin1.pull = digitalio.Pull.DOWN

CLK_Pin1 = digitalio.DigitalInOut(board.GP13)
CLK_Pin1.direction = digitalio.Direction.INPUT
CLK_Pin1.pull = digitalio.Pull.DOWN

SW1 = digitalio.DigitalInOut(board.GP14)
SW1.direction = digitalio.Direction.INPUT
SW1.pull = digitalio.Pull.DOWN


#___________________Rotary Encoder Function______________________
previousValue = 1
def rotary_changed_left():
    global previousValue
    if previousValue != CLK_Pin1.value:
        if CLK_Pin1.value == 0:
            if DT_Pin1.value == 0:
                return(False)
            else:   
                return(True)     
        previousValue = CLK_Pin1.value
    return(None)
    
#__________________________________________________________________________________________
#_________________List of defind mode names, change the modes as you need_________________

mode_names = {1 : 'Blender', 2 : 'Windows', 3 : 'Premier Pro', 4 : "After Effects", 5 : "Fusion360"}

# Set Default Mode To 1
mode = 0
        
print(mode_names[1])        

# Function to update the macro label on the OLED screen
def update_macro_label(macro_name):
    macro_label = label.Label(terminalio.FONT, text=macro_name, color=0xFFFF00, x=0, y=55)
    splash.append(macro_label)
    display.refresh()
    time.sleep(3)
    splash.remove(macro_label)
    display.refresh()

while True:

    x = get_voltage(x_axis)
    y = get_voltage(y_axis)

    if select.value is False:
        mouse.click(Mouse.LEFT_BUTTON)
        time.sleep(0.2)  # Debounce delay

    if steps(x) > 11.0:
        # print(steps(x))
        mouse.move(x=1)
    if steps(x) < 9.0:
        # print(steps(x))
        mouse.move(x=-1)

    if steps(x) > 19.0:
        # print(steps(x))
        mouse.move(x=8)
    if steps(x) < 1.0:
        # print(steps(x))
        mouse.move(x=-8)

    if steps(y) > 11.0:
        # print(steps(y))
        mouse.move(y=-1)
    if steps(y) < 9.0:
        # print(steps(y))
        mouse.move(y=1)

    if steps(y) > 19.0:
        # print(steps(y))
        mouse.move(y=-8)
    if steps(y) < 1.0:
        # print(steps(y))
        mouse.move(y=8)
    
    if modeChangeButton.value:
        mode = mode + 1
        if mode > 5:
            mode = 1
        time.sleep(1)
        
        # Make the display context
        splash = displayio.Group()
        display.show(splash)

        color_bitmap = displayio.Bitmap(128, 64, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0xFFFFFF  # White

        bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        splash.append(bg_sprite)

        # Draw a smaller inner rectangle
        inner_bitmap = displayio.Bitmap(118, 54, 1)
        inner_palette = displayio.Palette(1)
        inner_palette[0] = 0x000000  # Black
        inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=5)
        splash.append(inner_sprite)

        # Draw a label
        text = mode_names[mode]
        center_x = (118 - len(text) * 6) // 2 + 5
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=center_x, y=28)
        splash.append(text_area)
    
#----------------------------------------MODE 1--------------------------------------------------------------------------
        
    if mode == 0:
        time.sleep(0.01)
        
    if mode == 1:
        blender_mode_handle_keypress(key, cc, write_text, keyboard, SW1, rotary_changed_left,splash, display)
        
    elif mode == 2:
        windows_mode_handle_keypress(key, cc, write_text, keyboard, SW1,rotary_changed_left, splash, display)
        
    elif mode == 3:
        premier_mode_handle_keypress(key, cc, write_text, keyboard, SW1, rotary_changed_left, splash, display)

    elif mode == 4:
        aftereffects_mode_handle_keypress(key, cc, write_text, keyboard, SW1,rotary_changed_left, splash, display)
        
    elif mode == 5:
        fusion360_mode_handle_keypress(key, cc, write_text, keyboard, SW1,rotary_changed_left, splash, display)
              
    time.sleep(0.001)
```

To create your own macro for a specific software you need to follow the following process.

**Part 1: Creating the Custom Mode File** To begin, we'll create a new Python file for our custom mode. Let's name it `my_custom_mode.py`. Inside this file, we'll define a function called `handle_keypress` to handle the keypresses and execute macros specific to our custom mode. Here's an example of how `my_custom_mode.py` might look:

```python
import time
import board, busio, displayio, os, terminalio
import digitalio
import time
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_display_text import label
import adafruit_displayio_ssd1306

def update_screen(splash, macro_name, display):
    # Update the macro label
    center_x = (118 - len(macro_name) * 6) // 2 + 5
    macro_label = label.Label(terminalio.FONT, text=macro_name, color=0xFFFF00, x=center_x, y=50)
    splash.append(macro_label)
    display.refresh()
    # Wait for 1 seconds
    time.sleep(1)
    # Remove the macro label after 1 seconds
    splash.remove(macro_label)
    display.refresh()
    
def handle_keypress(key, cc, write_text, keyboard, SW1, SW2, rotary_changed_left, rotary_changed_right, splash, display ):
    
    # Macro names or actions
    # Change the macro names * 
    macro_names = {
        0: "*",
        1: "*",
        2: "*",
        3: "*",
        4: "*",
        5: "*",
        6: "*",
        7: "*",
        8: "*",
        9: "*",
        10: "*",
        11: "*",
        # Add more macro names and their corresponding keys as needed
    }
    
    #Replace keyboard.send(Keycode.G) with your macro code
    
    if key[0].value:
        keyboard.send(Keycode.G)
        time.sleep(0.2)
        update_screen(splash, macro_names[0], display)
         
    if key[1].value:
        keyboard.send(Keycode.G)
        time.sleep(0.2)
        update_screen(splash, macro_names[1], display)
        
    if key[2].value:
        keyboard.send(Keycode.G)
        time.sleep(0.2)
        update_screen(splash, macro_names[2], display)
    
    if key[3].value:
        cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        time.sleep(0.2)
        update_screen(splash, macro_names[3], display)
    
    if key[4].value:
        keyboard.send(Keycode.G)
        time.sleep(0.3)
        update_screen(splash, macro_names[4], display)
        
    if key[5].value:
        keyboard.send(Keycode.G)
        time.sleep(0.3)
        update_screen(splash, macro_names[5], display)

    if key[6].value:
        keyboard.send(Keycode.G)
        time.sleep(0.3)
        update_screen(splash, macro_names[6], display)
        
    if key[7].value:
        keyboard.send(Keycode.G)
        time.sleep(0.3)
        update_screen(splash, macro_names[7], display)
        
    if key[8].value:
        keyboard.send(Keycode.G)
        time.sleep(0.3)
        update_screen(splash, macro_names[8], display)
         
    if key[9].value:
        keyboard.send(Keycode.G)
        time.sleep(0.3)
        update_screen(splash, macro_names[9], display)
        
    if key[10].value:
        keyboard.send(Keycode.G)
        time.sleep(0.3)
        update_screen(splash, macro_names[10], display)
        
    if key[11].value:
        keyboard.send(Keycode.G)
        time.sleep(0.3)
        update_screen(splash, macro_names[10], display)
        
    #Rotary encoder 1 turned clockwise     
    if rotary_changed_left() == True:
        cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        time.sleep(0.01)
        
    elif rotary_changed_left() == False:
        cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        time.sleep(0.01)
    
    #Rotary encoder 2 turned clockwise
    if rotary_changed_right() == True:
        cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        time.sleep(0.01)
         
    elif rotary_changed_right() == False:
        cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        time.sleep(0.01)
            
    if not SW1.value:
        keyboard.send(Keycode.G)
        time.sleep(0.2)
        
    if not SW2.value:
        keyboard.send(Keycode.G)
        time.sleep(0.2)

    time.sleep(0.0001)
```

Now that we have our custom mode defined in `my_custom_mode.py`, let's import it into the `code.py` script to make it an integral part of our macro keyboard. Here's how you can import the custom mode:

```python
# code.py
# Import the custom mode
from my_custom_mode import handle_keypress as my_custom_mode_handle_keypress
```

**Adding the Custom Mode to mode\_names Dictionary** For better user experience, we should add our custom mode name to the `mode_names` dictionary so that it appears on the OLED display. Let's update the dictionary in the `code.py` script:

```
# List of predefined modes and their associated functions
mode_names = {1: 'Blender', 2: 'Windows', 3: 'Premier Pro', 4: "After Effects", 5: "Fusion360", 6: "My Custom Mode"}
```

If you do find anything difficult or do not understand what is going on, you can reach me on YouTube or ask questions in the Discord community

Please share any improvements you made with the code to the community so that I can share it.

## Enclosure Design

The enclosure was made in Fusion360. The enclosure consist of top and bottom part which will be fixed to the PCB through M3 Brass HEX standoffs and screws



<figure><img src="images/enclosure_top.png" alt=""><figcaption></figcaption></figure>

<figure><img src="images/enclosure_bottom.png" alt=""><figcaption></figcaption></figure>



If anyone decides to recreate this project and comes up with an improved design for the case, please feel free to share it with me. I would love to see what you create!

## Conclusion

This macrokeyboard series is an ongoing project, and based on your feedback I will create a new version.
