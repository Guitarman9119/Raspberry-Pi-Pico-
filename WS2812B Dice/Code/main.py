from machine import Pin
import neopixel
import utime
import urandom
  
# --- CONFIG ---
NUM_LEDS = 14
PIN_NUM = 11
BRIGHTNESS = 1           # 0.0 = off, 1.0 = full brightness
LEFT_COLOR = (0, 0, 255)     # Magenta
RIGHT_COLOR = (255, 150, 255)  # Light pink
RAINBOW_DELAY = 0.02

# --- SETUP ---
np = neopixel.NeoPixel(Pin(PIN_NUM), NUM_LEDS)
urandom.seed(utime.ticks_us())

dice1_leds = list(range(0, 7))
dice2_leds = list(range(7, 14))

numbers = [
    [0, 0, 0, 1, 0, 0, 0],  # 1
    [1, 0, 0, 0, 0, 0, 1],  # 2
    [1, 0, 0, 1, 0, 0, 1],  # 3
    [1, 1, 0, 0, 0, 1, 1],  # 4
    [1, 1, 0, 1, 0, 1, 1],  # 5
    [1, 1, 1, 0, 1, 1, 1],  # 6
]

button1 = Pin(12, Pin.IN, Pin.PULL_DOWN)
button2 = Pin(13, Pin.IN, Pin.PULL_DOWN)
button3 = Pin(14, Pin.IN, Pin.PULL_DOWN)

# --- HELPER FUNCTIONS ---
def apply_brightness(color, brightness):
    """Apply brightness scaling to any RGB color tuple."""
    return tuple(int(c * brightness) for c in color)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return (int(pos * 3), int(255 - pos * 3), 0)
    elif pos < 170:
        pos -= 85
        return (int(255 - pos * 3), 0, int(pos * 3))
    else:
        pos -= 170
        return (0, int(pos * 3), int(255 - pos * 3))

def rainbow_cycle(wait, brightness, cycles=1):
    """Cycle rainbow colors across all LEDs with brightness scaling."""
    for j in range(256 * cycles):
        for i in range(NUM_LEDS):
            rc_index = (i * 256 // NUM_LEDS) + j
            color = wheel(rc_index & 255)
            np[i] = apply_brightness(color, brightness)
        np.write()
        utime.sleep(wait)
        # Exit rainbow if any button pressed
        if button1.value() or button2.value() or button3.value():
            return

def turn_off_leds(indices):
    for i in indices:
        np[i] = (0, 0, 0)
    np.write()

def show_number(indices, number, color, brightness):
    pattern = numbers[number - 1]
    adjusted = apply_brightness(color, brightness)
    for i in range(len(indices)):
        np[indices[i]] = adjusted if pattern[i] else (0, 0, 0)
    np.write()

def roll_animation_simultaneous(indices1, indices2, color1, color2, brightness):
    """Roll both dice at the same time with different colors."""
    delay = 0.02
    rolls = urandom.randint(8, 14)
    for _ in range(rolls):
        num1 = urandom.randint(1, 6)
        num2 = urandom.randint(1, 6)
        show_number(indices1, num1, color1, brightness)
        show_number(indices2, num2, color2, brightness)
        utime.sleep(delay)
        np.fill((0, 0, 0))
        np.write()
        delay += 0.03  # Gradually slow both down together

    # Final results
    final1 = urandom.randint(1, 6)
    final2 = urandom.randint(1, 6)
    show_number(indices1, final1, color1, brightness)
    show_number(indices2, final2, color2, brightness)
    return final1, final2

# --- MAIN LOOP ---
try:
    while True:
        if button1.value():
            utime.sleep(0.2)
            if button1.value():
                roll_animation_simultaneous(dice1_leds, [], LEFT_COLOR, RIGHT_COLOR, BRIGHTNESS)
                utime.sleep(2)
                turn_off_leds(dice1_leds)

        elif button2.value():
            utime.sleep(0.2)
            if button2.value():
                roll_animation_simultaneous(dice1_leds, dice2_leds, LEFT_COLOR, RIGHT_COLOR, BRIGHTNESS)
                utime.sleep(2)
                turn_off_leds(dice1_leds)
                turn_off_leds(dice2_leds)

        elif button3.value():
            utime.sleep(0.2)
            if button3.value():
                roll_animation_simultaneous([], dice2_leds, LEFT_COLOR, RIGHT_COLOR, BRIGHTNESS)
                utime.sleep(2)
                turn_off_leds(dice2_leds)

        else:
            # Idle rainbow animation when no button pressed
            rainbow_cycle(RAINBOW_DELAY, BRIGHTNESS, cycles=10)

        

except KeyboardInterrupt:
    np.fill((0, 0, 0))
    np.write()
    print("Stopped")
