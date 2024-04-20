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
    # Wait for 3 seconds
    time.sleep(1)
    # Remove the macro label after 3 seconds
    splash.remove(macro_label)
    display.refresh()
    
    

def handle_keypress(key, cc, write_text, keyboard, SW1, SW2, rotary_changed_left, rotary_changed_right, splash, display ):
    
    # Macro names or actions
    macro_names = {
        0: "Play / Pause",
        1: "Play/Pause",
        2: "Open Chrome",
        3: "Volume Up",
        4: "Grab",
        # Add more macro names and their corresponding keys as needed
    }
    
    
    if key[0].value:
        cc.send(ConsumerControlCode.PLAY_PAUSE)
        time.sleep(0.1)
        update_screen(splash, macro_names[0], display)
        
        
    if key[1].value:
        cc.send(ConsumerControlCode.PLAY_PAUSE)
        time.sleep(0.3)
        
        
    if key[2].value:
        keyboard.send(Keycode.SHIFT, Keycode.A)
        time.sleep(0.4)
        write_text.write('chrome\n')
        time.sleep(0.2)
        write_text.write('\n')
        time.sleep(1)
        write_text.write('https://www.youtube.com/watch?v=dQw4w9WgXcQ?autoplay=1\n')
    
    
    if key[3].value:
        cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        time.sleep(0.2)
    
    
    if key[4].value:
        keyboard.send(Keycode.G)
       
        time.sleep(0.3)
        
        
        
    #Rotary encoder 1 turned clockwise     
    if rotary_changed_left() == True:
        cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        time.sleep(0.01)
        
        
        
        
    elif rotary_changed_left() == False:
        cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        time.sleep(0.01)
       
    
    
    #Rotary encoder 2 turned clockwise
    if rotary_changed_right() == True:
        cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        time.sleep(0.01)
        
        
        
    elif rotary_changed_right() == False:
        cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        time.sleep(0.01)
        
        
        
    if not SW1.value:
        keyboard.send(Keycode.RIGHT_ARROW)
        print("Rotary 1 - Button pressed")
        time.sleep(0.2)
        
    if not SW2.value:
        print("Rotary 2 - Button pressed")
        time.sleep(0.2)
        



    time.sleep(0.0001)