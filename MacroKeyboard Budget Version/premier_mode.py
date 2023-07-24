import time
import digitalio
import time
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode


def handle_keypress(key, cc, write_text, keyboard, SW1, SW2, rotary_changed_left, rotary_changed_right, splash, display):
    
    
    if key[0].value:
        cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        time.sleep(0.1)
        
        
    if key[1].value:
        cc.send(ConsumerControlCode.PLAY_PAUSE)
        time.sleep(0.3)
        
    if key[2].value:
        keyboard.send(Keycode.GUI)
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
        print("test")
        keyboard.send(Keycode.N)
        time.sleep(0.3)
        
        
        
    #Rotary encoder turned clockwise
       
    if rotary_changed_left() == True:
        keyboard.send(Keycode.RIGHT_ARROW)
        
        
        
        
    elif rotary_changed_left() == False:
        keyboard.send(Keycode.LEFT_ARROW)
    
    #Rotary encoder turned clockwise
    if rotary_changed_right() == True:
        cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        time.sleep(0.01)
        
        
        
    elif rotary_changed_right() == False:
        cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        time.sleep(0.01)
        
        
    if not SW1.value:
        print("Rotary 1 - Button pressed")
        time.sleep(0.2)
        
    if not SW2.value:
        print("Rotary 2 - Button pressed")
        time.sleep(0.2)
        

    time.sleep(0.0001)
