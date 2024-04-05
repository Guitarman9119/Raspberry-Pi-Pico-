# Code Adapted from: 2018 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials HID Mouse example"""
import time
import analogio
import board
import digitalio
import usb_hid
from adafruit_hid.mouse import Mouse

# Define constants
POT_MIN = 0.00
POT_MAX = 3.29
STEP = (POT_MAX - POT_MIN) / 20.0
MOUSE_THRESHOLD_LOW = 9.0
MOUSE_THRESHOLD_MEDIUM = 15.0
MOUSE_THRESHOLD_HIGH = 19.0
MOUSE_STEP_LOW = 1
MOUSE_STEP_MEDIUM = 4
MOUSE_STEP_HIGH = 8

# Setup
mouse = Mouse(usb_hid.devices)
x_axis = analogio.AnalogIn(board.GP27)
y_axis = analogio.AnalogIn(board.GP26)
select = digitalio.DigitalInOut(board.GP16)
select.direction = digitalio.Direction.INPUT
select.pull = digitalio.Pull.UP

def get_voltage(pin):
    return (pin.value * 3.3) / 65536

def steps(axis):
    """ Maps the potentiometer voltage range to 0-20 """
    return round((axis - POT_MIN) / STEP)

def calculate_movement(axis):
    """ Calculates movement based on the step value """
    movement = 0
    if steps(axis) > MOUSE_THRESHOLD_HIGH:
        movement = MOUSE_STEP_HIGH
    elif steps(axis) > MOUSE_THRESHOLD_MEDIUM:
        movement = MOUSE_STEP_MEDIUM
    elif steps(axis) > MOUSE_THRESHOLD_LOW:
        movement = MOUSE_STEP_LOW
    elif steps(axis) < MOUSE_THRESHOLD_LOW:
        movement = - MOUSE_STEP_LOW
    elif steps(axis) < MOUSE_THRESHOLD_MEDIUM:
        movement = - MOUSE_STEP_MEDIUM
    elif steps(axis) < MOUSE_THRESHOLD_HIGH:
        movement = - MOUSE_STEP_HIGH
    return movement

# Main loop
while True:
    x = get_voltage(x_axis)
    y = get_voltage(y_axis)

    if not select.value:
        mouse.click(Mouse.LEFT_BUTTON)
        time.sleep(0.2)  # Debounce delay

    x_move = calculate_movement(x)
    y_move = - calculate_movement(y)  # Invert y value for standard orientation

    mouse.move(x=x_move, y=y_move)