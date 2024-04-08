# Learning Board - GitHub

Introducing a new way to learn how to use the Raspberry Pi Pico, focusing on **coding** and learning about **electronic sensors** and **modules**. I created a series of **PCB learning boards** that will make the process easier to learn **electronics and programming.**

As a teacher I understand that constructing circuits on breadboards can be time-consuming and frustrating, especially for beginners. That's why I designed PCB boards to be easily swappable and interchangeable, allowing students to focus on coding and practical usage of sensors and different modules through coding using **MicroPython** or **CircuitPython** without worrying about complicated wiring. The idea is learn coding and how different sensors work and their application before constructing on a breadboard and building your own projects.

The boards are perfect for students of all ages and skill levels, providing an introduction to microcontrollers that is both fun and educational. Each PCB Shield board is designed to focus on specific sensors or modules, with a series of lessons that teach you about the components (sensor / module), how it work, and how to program the Pico in either **MicroPython** or **CircuitPython**.

Once you've mastered the basics, you can choose to build the circuit yourself using a **provided diagram**, or just use the board in the project your are building.

The Raspberry Pi Pico was chosen due to the availability, low-price and support for MicroPython which is easier to learn compared to C++ for beginners. The raspberry Pi Pico will be plugged into the "Main Motherboard" which will then use female header pins where other PCB boards will be plugged in. At the time of writing this Instructable I have made 3 different custom boards as shown in Figure above and I will discuss the usage of each PCB board, and provide the lessons down below. The worksheets and book for this is a work in progress, and to have a more updated progress visit my [website](http://www.nerdcave.xyz/) or come back to this instructable for an update.

### Supplies

**Components and Quantity**

10mm LED (Any color) - 16

SSD1306 OLED - 1

Passive Buzzer -1

Resistor 330 Ohm -16

Push Button 12x12mm - 3

Female Header Pins - 4 x 20 pin 2.54mm

Male Header Pins - 4 x (20 pin (2.54 mm)) , 2 x (4 pin (2.54 mm)) , 1 x (5 pin (2.54 mm))

**Where to Buy the learning "Pico Learning Boards?"**

The board is open source and you can order the PCB using any PCB manufacturer. I recommend using [JLCPCB](https://jlcpcb.com/?from=Nerd) who is a sponsor of the YouTube channel NerdCave of which I manage and create content for. Use the link provided which is a referral link that will support me as a creator to keep making content that is assessable and open source at no charge to you. I am planning on selling the boards as a kit which you can buy in future. This will support the channel and project.&#x20;

### Step 1: Raspberry Pi Pico

[![Raspberry Pi Pico](https://content.instructables.com/FOI/3MMA/LQQNAAWR/FOI3MMALQQNAAWR.png?auto=webp\&frame=1\&width=1024\&fit=bounds\&md=a0879270c274914b060398978022ae3c)](https://content.instructables.com/FOI/3MMA/LQQNAAWR/FOI3MMALQQNAAWR.png?auto=webp\&frame=1\&width=1024\&fit=bounds\&md=a0879270c274914b060398978022ae3c)

The Raspberry Pi Pico is a compact, low-cost, high-performance microcontroller board developed by the Raspberry Pi Foundation. It’s designed to provide a flexible and accessible platform for both beginners and professionals to create a wide range of digital projects and applications.

\


#### Key Features&#x20;

* RP2040 Microcontroller Chip: The Pico is powered by Raspberry Pi’s first microcontroller chip, the RP2040, which features a dual-core ARM Cortex M0+ processor, flexible clock running up to 133MHz.
* Memory and Storage: It comes with 264KB of SRAM, and 2MB of on-board Flash memory, providing ample space for your applications.
* Versatile I/O: The Pico provides a wide range of I/O options, including 26 multifunction GPIO pins, 3 analogue inputs, and a variety of interface support like I2C, SPI, and UART.
* On-board Temperature Sensor: An integrated temperature sensor provides a way for applications to respond to changes in ambient conditions.
* Castellated Module: The Pico’s castellated module allows soldering directly to carrier boards, making it an excellent choice for both prototype and production.
* Micro-USB B Port: The Pico can be powered and programmed via a micro-USB B port, making it easy to connect to a wide range of devices.

#### Applications&#x20;

The Raspberry Pi Pico is a versatile platform suitable for a wide range of applications, including:

* \-Internet of Things (IoT) Devices: With its low power consumption and wide range of I/O options, the Pico is an excellent choice for IoT devices.
* Embedded Systems: The Pico’s compact size and powerful microcontroller make it ideal for embedded systems.
* Robotics: The Pico can be used to control a wide range of robotic systems, from simple hobbyist projects to complex industrial applications.
* Education: With its low cost and easy-to-use design, the Pico is an excellent tool for teaching programming and electronics.

Whether you’re a hobbyist looking to experiment with electronics, a professional developing a new product, or an educator teaching the next generation of programmers, the Raspberry Pi Pico offers a powerful and flexible platform for your needs.

### Step 2: Ordering Learning Board (JLCPCB)

[![Ordering Learning Board (JLCPCB)](https://content.instructables.com/FEJ/26M4/LQQNA8UH/FEJ26M4LQQNA8UH.png?auto=webp\&frame=1\&width=700\&fit=bounds\&md=ad9532c40ec352e1ed9c01fc4096421f)](https://content.instructables.com/FEJ/26M4/LQQNA8UH/FEJ26M4LQQNA8UH.png?auto=webp\&frame=1\&fit=bounds\&md=ad9532c40ec352e1ed9c01fc4096421f)[![Ordering Learning Board (JLCPCB)](https://content.instructables.com/FK6/7Z5D/LQQNA8V9/FK67Z5DLQQNA8V9.png?auto=webp\&frame=1\&width=419\&fit=bounds\&md=a4e1b8879a75fbe8b10053637fbd3209)](https://content.instructables.com/FK6/7Z5D/LQQNA8V9/FK67Z5DLQQNA8V9.png?auto=webp\&frame=1\&fit=bounds\&md=a4e1b8879a75fbe8b10053637fbd3209)[![Ordering Learning Board (JLCPCB)](https://content.instructables.com/F3H/KQTN/LQQNABI8/F3HKQTNLQQNABI8.png?auto=webp\&frame=1\&crop=3:2\&width=419\&fit=bounds\&md=1afedc60ba931a891d4480b152aa772c)](https://content.instructables.com/F3H/KQTN/LQQNABI8/F3HKQTNLQQNABI8.png?auto=webp\&frame=1\&width=1024\&fit=bounds\&md=1afedc60ba931a891d4480b152aa772c)2 More Images

The PCB was ordered through JLCPCB. They offer great PCBs at a low cost and have promotions and coupons available throughout the year.

**Ordering the PCB is very simple:**

Download the Gerber using the link: [PCB](https://github.com/Guitarman9119/Raspberry-Pi-Pico-/tree/main/Raspberry%20Pi%20Pico%20Learning%20Board%20Project)

**Sign up through**[https://jlcpcb.com/?from=Nerd](https://jlcpcb.com/?from=NerdCave)

* Click on Add Gerber file
* Leave all the settings as default given. You might want change the PCB color.
* Finally save to cart, enter your shipping details and order the PCB

### Step 3: Installing MicroPython

Start with your Pico unplugged from USB. Hold down the **BOOTSEL** button, and while continuing to hold it (don't let go!), plug the Pico into USB. A short GIF above illustrates this step. **Continue to hold the BOOTSEL button until the RPI-RP2 drive appears.**

Drag the **rp2-pico-20220117-v1.18.uf2** [file](https://github.com/Guitarman9119/Raspberry-Pi-Pico-/tree/main/Pico%20Alarm%20Clock) to **RPI-RP2.**

Alternative method will be using Thonny to install MicroPython. If you are completely new to the Raspberry Pi Pico do not fear there are many videos and tutorials on getting started and I have included a tutorial here which you can find on my YouTube channel ([Link](https://youtu.be/qYqUJC9z2\_E)).

### Step 4: Learning Board 1

[![Learning Board 1](https://content.instructables.com/F79/8NR6/LQQNA7MR/F798NR6LQQNA7MR.jpg?auto=webp\&frame=1\&width=617\&height=1024\&fit=bounds\&md=3673851a2f959499be38886253f953b7)](https://content.instructables.com/F79/8NR6/LQQNA7MR/F798NR6LQQNA7MR.jpg?auto=webp\&frame=1\&width=1024\&height=1024\&fit=bounds\&md=3673851a2f959499be38886253f953b7)[![Learning Board 1](https://content.instructables.com/F6A/JZ1N/LQQNAE9C/F6AJZ1NLQQNAE9C.png?auto=webp\&frame=1\&width=583\&fit=bounds\&md=29e3b64f689b873c91e9e15b2539fc8f)](https://content.instructables.com/F6A/JZ1N/LQQNAE9C/F6AJZ1NLQQNAE9C.png?auto=webp\&frame=1\&width=1024\&fit=bounds\&md=29e3b64f689b873c91e9e15b2539fc8f)

Board 1 - consists of a few **input** and **output** devices. To get you started learning the Raspberry Pi Pico. From this board, we will do 7 Simple Lessons. You can easily change the task to fit your students need or create more lessons. The Gerber file to learning board 1 is available to download here:

### Electronic Components Review:

A short overview of each component is given in this instructable.

**LED**

* Description: A semiconductor light source that emits light when an electric current flows through it. LEDs are commonly used as indicators in electronic circuits.
* How it works: It emits light when electrons recombine with electron holes in the device, releasing energy in the form of photons.
* Usage: Indicators, display elements, illumination.

**Resistor**

* Description: A passive two-terminal electronic component that resists the flow of electric current.
* How it works: It limits the current flowing through a circuit and is characterized by its resistance value.
* Usage: Current limiting, voltage division, setting bias points.

**Push Button**

* Description: A switch that is activated by pushing it.
* How it works: Completes or interrupts an electric circuit when pressed.
* Usage: User input, toggling, control switches.

**HC-SR04 Ultrasonic Sensor**

* Description: An ultrasonic ranging module that measures distance using ultrasonic waves.
* How it works: Sends ultrasonic pulses and measures the time taken for the echo to return to calculate distance.
* Usage: Distance measurement, object detection.

**Passive Buzzer**

* Description: An audio signaling device that does not generate a tone on its own.
* How it works: It requires an external waveform to produce sound.
* Usage: Alarms, notifications, simple sound generation.

**SSD1306 0.96 inch**

* Description: A small OLED (Organic Light Emitting Diode) display.
* How it works: Each pixel is a small organic LED, and the display emits light when an electric current is applied.
* Usage: Display information, graphics, user interface.

### &#x20;

### Step 5: Learning Board 1 - Lesson 1 - Controlling LED's

### Introduction

Welcome to the first lesson of our Raspberry Pi Pico learning series. In this lesson, we will explore how to control LEDs using the Raspberry Pi Pico. LEDs are a fundamental component in electronics, and learning how to control them is a crucial step in understanding how to interact with hardware using software.

We will be using the MicroPython programming language, which is a lean and efficient implementation of Python 3 that includes a small subset of Python standard library and is optimized to run on microcontrollers.

By the end of this lesson, you will be able to control the 16 LEDs connected to your learning board, turning them on and off programmatically. This will give you a solid foundation for creating more complex projects in the future.

### Code

```python
from time import sleep

def blink_all_leds(times, delay=0.5):
    for _ in range(times):
        set_all_leds(1)
        sleep(delay)
        set_all_leds(0)
        sleep(delay)
```

### Code with Explanation

First, we need to import the Pin class from the machine module. This class provides access to GPIO (General Purpose Input/Output) pins, which we will use to control the LEDs.

```python
from machine import Pin
```

Next, we will create an array of Pin objects for each of the LEDs. The LEDs are connected to GPIO pins from GP0 to GP15, so we will create 16 Pin objects. We set the Pin objects as output pins by passing Pin.OUT as the second argument.

```python
leds = [Pin(i, Pin.OUT) for i in range(16)]
```

Now, we can control the LEDs by setting their value to 1 (on) or 0 (off). For example, to turn on the LED connected to GP0, we can do:

```python
leds[0].value(1)
```

And to turn it off:

```python
leds[0].value(0)
```

Let's create a function that turns all LEDs on or off:

```python
def set_all_leds(value):
    for led in leds:
        led.value(value)
```

Now, we can turn all LEDs on with set\_all\_leds(1) and off with set\_all\_leds(0).

Finally, let's create a function that makes the LEDs blink. We will use the sleep function from the time module to pause execution for a specified number of seconds.

```python
from time import sleep

def blink_all_leds(times, delay=0.5):
    for _ in range(times):
        set_all_leds(1)
        sleep(delay)
        set_all_leds(0)
        sleep(delay)
```

You can call blink\_all\_leds(5) to make all LEDs blink 5 times with a delay of 0.5 seconds between each blink.

That's it! You now know how to control LEDs with the Raspberry Pi Pico.

### Step 6: Learning Board 1 - Button + LED Control

### Introduction

Welcome to the second lesson of our Raspberry Pi Pico learning series. In this lesson, we will learn how to interact with push buttons using the Raspberry Pi Pico. Push buttons are simple yet essential components in electronics, allowing us to provide input to our devices.

We will continue using the MicroPython programming language, leveraging its simplicity and power to control our hardware.

By the end of this lesson, you will be able to read the state of the three buttons connected to your learning board, and use this input to control the LEDs we learned about in the previous lesson.

### Code

```python
from machine import Pin
buttons = [Pin(i, Pin.IN, Pin.PULL_UP) for i in range(20, 23)]
if buttons[0].value() == 0:
    print("Button 0 is pressed")
def check_buttons():
    for i in range(3):
        if buttons[i].value() == 0:
            set_all_leds(1)
            print(f"Button {i} is pressed")
        else:
            set_all_leds(0)
while True:
    check_buttons()
```

### Code with Explanation

First, we need to import the Pin class from the machine module, if it's not already imported.

```python
from machine import Pin
```

Next, we will create a Pin object for each of the buttons. The buttons are connected to GPIO pins GP20, GP21, and GP22. We set the Pin objects as input pins by passing Pin.IN as the second argument.

```python
buttons = [Pin(i, Pin.IN, Pin.PULL_UP) for i in range(20, 23)]
```

We use Pin.PULL\_UP because the buttons are wired in a pull-up resistor configuration. This means that when the button is not pressed, the input pin will be pulled to a high voltage level (logic 1). When the button is pressed, it will be connected to ground, and the input pin will read a low voltage level (logic 0).

To read the state of a button, we can use the value method. For example, to check if the first button is pressed, we can do:

```python
if buttons[0].value() == 0:
    print("Button 0 is pressed")
```

Now, let's create a function that turns on an LED when a button is pressed. We will use the LEDs and the set\_all\_leds function from the previous lesson.

```python
def check_buttons():
    for i in range(3):
        if buttons[i].value() == 0:
            set_all_leds(1)
            print(f"Button {i} is pressed")
        else:
            set_all_leds(0)
```

This function checks the state of each button. If a button is pressed, it turns on all LEDs and prints a message. Otherwise, it turns off all LEDs.

Finally, let's create a loop that continuously checks the state of the buttons:

```python
while True:
    check_buttons()
```

This will keep the program running indefinitely, constantly checking if any button is pressed and reacting accordingly.

Congratulations! You now know how to interact with push buttons using the Raspberry Pi Pico.

\


### Step 7: Learning Board 1 -Buzzer + Simple Tone Generator

### Introduction

Welcome to the third lesson of our Raspberry Pi Pico learning series. In this lesson, we will learn how to use a buzzer with the Raspberry Pi Pico and MicroPython. A buzzer is a simple yet versatile component that can be used to play different tones and sounds, providing auditory feedback or simple melodies.

We will explore how to generate different tones using Pulse Width Modulation (PWM), a technique that involves varying the width of the pulses in a pulse train. By the end of this lesson, you will be able to play a simple song, "Twinkle, Twinkle, Little Star," on the buzzer.

### Code

```python
import machine
import utime
pwm_pin = machine.Pin(26)
pwm = machine.PWM(pwm_pin)
def play_note(frequency, duration):
    pwm.freq(int(frequency))
    pwm.duty_u16(32768)
    utime.sleep(duration)
    pwm.duty_u16(0)
twinkle_notes = [
    (261.63, 0.5),  # C4
    (261.63, 0.5),  # C4
    (392.00, 0.5),  # G4
    (392.00, 0.5),  # G4
    (440.00, 0.5),  # A4
    (440.00, 0.5),  # A4
    (392.00, 1.0),  # G4
    (349.23, 0.5),  # F4
    (349.23, 0.5),  # F4
    (329.63, 0.5),  # E4
    (329.63, 0.5),  # E4
    (293.66, 0.5),  # D4
    (293.66, 0.5),  # D4
    (261.63, 1.0)   # C4
]
for note in twinkle_notes:
    play_note(note[0], note[1])
    utime.sleep(0.1)
for note in twinkle_notes:
    play_note(note[0], note[1])
    utime.sleep(0.1)
pwm.deinit()

```

### Code with Explanation

First, we import the machine and utime modules. The machine module provides classes for hardware-specific operations, and utime provides functions for time-related operations.

```python
import machine
import utime
```

Next, we define the GPIO pin to which the buzzer is connected (GP26 in this case) and create a PWM object for this pin.

```python
pwm_pin = machine.Pin(26)
pwm = machine.PWM(pwm_pin)
```

We then define a function, play\_note, that takes a frequency and a duration as arguments. This function sets the frequency of the PWM signal to the frequency of the note, sets a default duty cycle to produce sound, waits for the duration of the note, and then sets the duty cycle to 0 to stop the sound.

```python
def play_note(frequency, duration):
    pwm.freq(int(frequency))
    pwm.duty_u16(32768)
    utime.sleep(duration)
    pwm.duty_u16(0)
```

We define the notes for "Twinkle, Twinkle, Little Star" as tuples of frequency (in Hz) and duration (in seconds).

```python
twinkle_notes = [
    (261.63, 0.5),  # C4
    (261.63, 0.5),  # C4
    (392.00, 0.5),  # G4
    ...
    (261.63, 1.0)   # C4
]
```

We then play the song by iterating over the notes and calling play\_note for each note. We introduce a short delay between notes with utime.sleep(0.1).

```python
for note in twinkle_notes:
    play_note(note[0], note[1])
    utime.sleep(0.1)
```

Finally, we clean up the PWM and GPIO resources with pwm.deinit().

```python
pwm.deinit()
```

Congratulations! You now know how to use a buzzer with the Raspberry Pi Pico and MicroPython.

### Step 8: Learning Board 1 - OLED Display

### Introduction

Welcome to the fourth lesson of our Raspberry Pi Pico learning series. In this lesson, we will learn how to use an OLED (Organic Light Emitting Diode) display with the Raspberry Pi Pico and MicroPython. An OLED display is a light-emitting diode in which the emissive electroluminescent layer is a film of organic compound that emits light in response to an electric current.

We will be using the SSD1306 OLED display, which is a small and versatile display with 128x64 pixels. By the end of this lesson, you will be able to display text on the OLED screen, which can be used to provide visual feedback, display sensor readings, or create simple user interfaces. In this example we will read onboard temperature sensor of the Raspberry Pi Pico.

### Code

```python
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf
import time
WIDTH = 128
HEIGHT = 64

i2c = I2C(0, scl = Pin(17), sda = Pin(16), freq=400000)
def read_temp():
    sensor_temp = machine.ADC(4)
    conversion_factor = 3.3 / (65535)
    reading = sensor_temp.read_u16() * conversion_factor 
    temperature = 27 - (reading - 0.706)/0.001721
    formatted_temperature = "{:.1f}".format(temperature)
    string_temperature = str("Temperature:" + formatted_temperature)
    print(string_temperature)
    time.sleep(2)
    return string_temperature
while True:
    display.text('Example 1:',0,0)
    temperature = read_temp()
    display.text(temperature,0,14)
    display.show()
    display.fill(0)
```

### Code with Explanation

First, we import the necessary modules. The machine module provides classes for hardware-specific operations, the ssd1306 module provides a driver for the SSD1306 OLED display, framebuf provides frame buffer support, and time provides functions for time-related operations.

```python
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf
import time
```

Next, we define the width and height of the display, and create an I2C object. The OLED display is connected to the I2C pins (SDA on Pin 15 and SCL on Pin 17).

```python
WIDTH = 128
HEIGHT = 64
i2c = I2C(0, scl = Pin(17), sda = Pin(16), freq=400000)
```

We then create an SSD1306\_I2C object for the display.

```python
display = SSD1306_I2C(WIDTH, HEIGHT, i2c)
```

We define a function, read\_temp, that reads the temperature from the built-in temperature sensor of the Raspberry Pi Pico, formats it as a string, and returns it.

```python
def read_temp():
    sensor_temp = machine.ADC(4)
    conversion_factor = 3.3 / (65535)
    reading = sensor_temp.read_u16() * conversion_factor 
    temperature = 27 - (reading - 0.706)/0.001721
    formatted_temperature = "{:.1f}".format(temperature)
    string_temperature = str("Temperature:" + formatted_temperature)
    print(string_temperature)
    time.sleep(2)
    return string_temperature
```

Finally, we create a loop that continuously updates the display with the current temperature. We use the text method of the SSD1306\_I2C object to draw text on the display, and the show method to update the display. We use the fill method with argument 0 to clear the display.

```python
while True:
    display.text('Example 1:',0,0)
    temperature = read_temp()
    display.text(temperature,0,14)
    display.show()
    display.fill(0)
```

Congratulations! You now know how to use an OLED display with the Raspberry Pi Pico and MicroPython.

### Step 9: Other Learning Boards

I am planning on making more learning boards in the future. The information provided in this GitHub should be enough to allow you to create your own version of learning boards based on the Raspberry Pi Pico. The other learning boards I have planned:

* Macro Keyboard board
* Logic Gates board
* Binary decoder
* Motor controller
* Relay Board
* 7 Segment Display Board
* MIDI Controller

The rest of boards will just be various of sensor boards.

### Step 10: Conclusion

This is a work in progress project, and will take a long time to have a polished textbook and worksheets, but I will constantly update the project on my website with resources, so visit my website for more updates and if you want to contribute please reach out to me.
