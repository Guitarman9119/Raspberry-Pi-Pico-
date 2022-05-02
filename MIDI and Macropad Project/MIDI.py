# This code is adapted from Liz Clark - MIDIFIGHTER project for Adafruit Industries - 
# https://learn.adafruit.com/raspberry-pi-pico-led-arcade-button-midi-controller-fighter

import time
import board
import terminalio
import busio
import digitalio
import usb_midi
import adafruit_midi
from adafruit_midi.note_on          import NoteOn
from adafruit_midi.note_off         import NoteOff


#  MIDI setup as MIDI out device
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

note_pins = [board.GP0, board.GP1,board.GP2,board.GP3,board.GP4,board.GP5,board.GP6,
             board.GP7,board.GP8,board.GP9,board.GP10,board.GP11,board.GP12,board.GP13,
             board.GP14,board.GP16]

note_buttons = []

for pin in note_pins:
    note_pin = digitalio.DigitalInOut(pin)
    note_pin.direction = digitalio.Direction.INPUT
    note_pin.pull = digitalio.Pull.DOWN
    note_buttons.append(note_pin)

#  note states
note0_pressed = False
note1_pressed = False
note2_pressed = False
note3_pressed = False
note4_pressed = False
note5_pressed = False
note6_pressed = False
note7_pressed = False
note8_pressed = False
note9_pressed = False
note10_pressed = False
note11_pressed = False
note12_pressed = False
note13_pressed = False
note14_pressed = False
note15_pressed = False

#  array of note states
note_states = [note0_pressed, note1_pressed, note2_pressed, note3_pressed,
               note4_pressed, note5_pressed, note6_pressed, note7_pressed,
               note8_pressed, note9_pressed, note10_pressed, note11_pressed,
               note12_pressed, note13_pressed, note14_pressed, note15_pressed]


#  array of default MIDI notes
midi_notes = [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75]


while True:

    #  MIDI input
    for i in range(16):
        buttons = note_buttons[i]
        #  if button is pressed...
        if buttons.value and note_states[i] is True:
            #  send the MIDI note and light up the LED
            midi.send(NoteOn(midi_notes[i], 120))
            note_states[i] = False
            print(midi_notes[i])
            
        #  if the button is released...
        if not buttons.value and note_states[i] is False:
            #  stop sending the MIDI note and turn off the LED
            midi.send(NoteOff(midi_notes[i], 120))
            note_states[i] = True
   

        

    

       

       
