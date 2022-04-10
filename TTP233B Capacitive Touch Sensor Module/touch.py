"""

TTP233B Touch sensor module demo

Remember to check out more tutorials on NerdCave - https://www.youtube.com/c/NerdCaveYT

Project Pinout
VCC - 3V3(OUT) (PIN36)
GND - GND (Any ground on Pico)
SIG - GP18 (PIN24)

"""

from machine import Pin
import time

Touch_pad = machine.Pin(18,Pin.IN,Pin.PULL_UP)

led = Pin(25,Pin.OUT)

while True:

    if Touch_pad.value()==1:

        print("Touched")

        led.toggle()

        time.sleep(0.5)