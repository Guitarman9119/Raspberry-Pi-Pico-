---
title: "Fibonnaci Clock"
description: "Raspberry Pi Pico W - Fibonnaci Clock"
lead: ""
date: 2020-10-06T08:48:57+00:00
lastmod: 2020-10-06T08:48:57+00:00
draft: false
images: []
menu:
weight: 501
---

## Introduction

Welcome to this tutorial on creating a Fibonacci Clock with the Raspberry Pi Pico W. The Fibonacci sequence is a series of numbers where each number is the sum of the two previous numbers. The first five numbers in the sequence are 1, 1, 2, 3, and 5. Using this sequence we can create a clock to show the the time in hours and minutes in increments of 5. 


<figure><img src="/fib1.png" alt=""><figcaption></figcaption></figure>


The screen of the clock is made up of five squares whose side lengths match the first five Fibonacci numbers: 1, 1, 2, 3 and 5. The hours are displayed using red and the minutes using green. When a square is used to display both the hours and minutes it turns blue. White squares are ignored. To tell time on the Fibonacci clock you need to do some math. To read the hour, simply add up the corresponding values of the red and blue squares. To read the minutes, do the same with the green and blue squares. The minutes are displayed in 5 minute increments (0 to 12) so you have to multiply your result by 5 to get the actual number.

### Component List

Here is the breakdown of components needed for the Macro Keyboard (assuming you have basic tools):

| Components          | Quantity            |
| ------------------- | ------------------- |
| Custom PCB          | 1                   |
| Raspberry Pi Pico W   | 1                   |
| WS2810B LED strip | +- 2 meter                  |
| 2.54 20 pin Header  | 2                   |
| Miscellaneous       | Depending on Design |

## Schematic Diagram

The schematic diagram was created using EasyEDA. All components used are through-hole types, making the soldering process easier and more accessible. The PCB allows us to easily connect the 5 different WS2812 neopixel LEDs to the Pico.  

<figure><img src="/ws2182_led_controller.png" alt=""><figcaption></figcaption></figure>

## PCB Design

Features of PCB

-   **Two Push Buttons:**  Two buttons are added to PCB, which could be used for brightness control, color change, or different modes
-   **Bluetooth Connector:**  An integrated connector for adding Bluetooth functionality via the HC-05 module, allowing for wireless control.
-   **Mounting Holes:**  The PCB is equipped with four 3mm mounting holes, making it easy to secure within an enclosure.


### PCB Top:

<figure><img src="/ws2818_pcb.png" alt=""><figcaption></figcaption></figure>



### Order PCB (JLCPCB)

The PCB was ordered through JLCPCB. They offer great PCBs at a low cost and have promotions and coupons available throughout the year. You can sign up using here, or using the following link:

[https://jlcpcb.com/?from=Nerd](https://jlcpcb.com/?from=NerdCave) that will support me as a creator to keep making content that is accessible and open source at no charge to you.

Ordering the PCB is very simple:

Download the Gerber file [here](https://github.com/Guitarman9119/Raspberry-Pi-Pico-/tree/main/WS2812B%20Controller).

Click on Add Gerber file

<figure><img src="/gerber.png" alt=""><figcaption></figcaption></figure>

leave all the settings as default given. You might want change the PCB color which you can do here:

<figure><img src="/pcb color.png" alt=""><figcaption></figcaption></figure>

Enter you shipping details, save to cart

<figure><img src="/Screenshot 2023-08-17 090943.png" alt=""><figcaption></figcaption></figure>

Then after a few days depending on your location you will receive your great quality PCB.

<figure><img src="/fib2.png" alt=""><figcaption></figcaption></figure>


## Code
 
In order to use the Fibonnaci Clock, you will have to create an account on IP Geolocation in order to access the API to get the correct time over Wifi. Visit the following tutorial to learn about it:  Before we dive into the code, you’ll need to set up an API key with the IP Geolocation API. Follow these steps to get your key:  [Tutorial](https://nerdcave.xyz/docs/tutorials/synchronize-time-over-wifi/)

Download the full demo code [here](https://github.com/Guitarman9119/Raspberry-Pi-Pico-/raw/refs/heads/main/Fibonacci%20clock/code.zip), which include the neopixel and urequest library.

### main.py
This is the main file that will be booted once your power the Pico. Comments is given in the code as detailed as possible and explained below.

```python
from machine import Pin, RTC  # Import necessary classes
import utime
import json
import network
import urequests
from neopixel import Neopixel  # Assuming you have the Neopixel class defined as in your previous code
import math

# Define the number of pixels for each strip (50 LEDs for each block)
numpix1 = 50  # Strip for Fibonacci number 1
numpix2 = 50  # Strip for Fibonacci number 1
numpix3 = 50  # Strip for Fibonacci number 2
numpix4 = 50  # Strip for Fibonacci number 3
numpix5 = 50  # Strip for Fibonacci number 5

# Create instances of Neopixel for each strip with fixed GPIO pins
strip1 = Neopixel(numpix1, 0, 1, "GRB")  # Strip 1 connected to GPIO 28
strip2 = Neopixel(numpix2, 1, 0, "GRB")  # Strip 2 connected to GPIO 29
strip3 = Neopixel(numpix3, 2, 2, "GRB")  # Strip 3 connected to GPIO 30
strip4 = Neopixel(numpix4, 3, 3, "GRB")  # Strip 4 connected to GPIO 31
strip5 = Neopixel(numpix5, 4, 4, "GRB")  # Strip 5 connected to GPIO 32

# Define colors
red = (255, 0, 0)      # Hours color
blue = (0, 0, 255)     # Minutes color
green = (0, 255, 0) # Both hours and minutes color
white = (255, 255, 255)      # Off color

# Set brightness for all strips
strip1.brightness(255)
strip2.brightness(255)
strip3.brightness(255)
strip4.brightness(255)
strip5.brightness(255)

# Load configuration
with open('config.json') as f:
    config = json.load(f)

# Check config.json has updated credentials
if config['ssid'] == 'Enter_Wifi_SSID':
    raise ValueError("config.json has not been updated with your unique keys and data")

# Your OpenWeatherMap API details
weather_api_key = config['weather_api_key']
city = config['city']
country_code = config['country_code']
date_time_api = config['date_time_api']
timezone = config['time_zone']

# Wi-Fi Configuration
def connect_wifi():
    with open('config.json') as f:
        config = json.load(f)
        weather_api_key = config['weather_api_key']
        city = config['city']
        country_code = config['country_code']
        date_time_api = config['date_time_api']
        timezone = config['time_zone']

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(config['ssid'], config['ssid_password'])

    print("Connecting to WiFi...")
    while not wlan.isconnected():
        utime.sleep(1)

    print("Connected to Wi-Fi:", wlan.ifconfig())
    
# Function to sync time with IP Geolocation API
def sync_time_with_ip_geolocation_api(rtc):
    url = f'http://api.ipgeolocation.io/timezone?apiKey={date_time_api}&tz={timezone}'
    response = urequests.get(url)
    data = response.json()

    # Print the full response to debug
    print("API Response:", data)

    if 'date_time' in data and 'timezone' in data:
        current_time = data["date_time"]
        print("Current Time String:", current_time)  # Debug print

        # Split the date and time directly from the returned format
        if " " in current_time:
            the_date, the_time = current_time.split(" ")
            year, month, mday = map(int, the_date.split("-"))
            hours, minutes, seconds = map(int, the_time.split(":"))

            week_day = data.get("day_of_week", 0)  # Default to 0 if not available
            rtc.datetime((year, month, mday, week_day, hours, minutes, seconds, 0))
            print("RTC Time After Setting:", rtc.datetime())
        else:
            print("Error: Unexpected time format:", current_time)
    else:
        print("Error: The expected data is not present in the response.")
        
# Initialize RTC (Real-Time Clock)
rtc = RTC()
connect_wifi()  # Connect to Wi-Fi
sync_time_with_ip_geolocation_api(rtc)  # Sync time from the API

# Fibonacci time function
def fib_time(hours, minutes):
    vals = [1, 1, 2, 3, 5]
    state = [0, 0, 0, 0, 0]

    # Calculate Fibonacci representation for hours
    remaining_hours = hours
    idx = len(vals) - 1
    for v in vals[::-1]:
        if remaining_hours == 0 or idx < 0: break
        if remaining_hours >= v:
            state[idx] += 1
            remaining_hours -= v
        idx -= 1

    # Calculate Fibonacci representation for minutes (in increments of 5)
    remaining_minutes = math.floor(minutes / 5)
    idx = len(vals) - 1
    for v in vals[::-1]:
        if remaining_minutes == 0 or idx < 0: break
        if remaining_minutes >= v:
            state[idx] += 2
            remaining_minutes -= v
        idx -= 1

    return state

# Main loop to update the NeoPixel LEDs based on the current time
while True:
    current_time = rtc.datetime()
    hours = current_time[4]%12  # Get hours
    minutes = current_time[5]  # Get minutes
    print(hours,minutes)
    state = fib_time(hours, minutes)
    
    print(state)
    # Update NeoPixel strips based on the state
    for i in range(5):
        if state[i] == 1:  # Hour representation
            # Light up the strip corresponding to the Fibonacci value for hours
            if i == 0:  # 1 hour
                strip1.fill(red)
            elif i == 1:  # 1 hour
                strip2.fill(red)
            elif i == 2:  # 2 hours (not applicable for 9:23)
                strip3.fill(red)
            elif i == 3:  # 3 hours (not applicable for 9:23)
                strip4.fill(red)
            elif i == 4:  # 5 hours (not applicable for 9:23)
                strip5.fill(red)
        elif state[i] == 2:  # Minute representation
            # Light up the strip corresponding to the Fibonacci value for minutes
            if i == 0:  # 1 minute
                strip1.fill(blue)
            elif i == 1:  # 1 minute
                strip2.fill(blue)
            elif i == 2:  # 2 minutes
                strip3.fill(blue)
            elif i == 3:  # 3 minutes
                strip4.fill(blue)
            elif i == 4:  # 5 minutes
                strip5.fill(blue)
        elif state[i] == 3:  # Both hour and minute representation
            # Light up the strip corresponding to the Fibonacci value for both
            if i == 0:  # 1 hour and 1 minute
                strip1.fill(green)
            elif i == 1:  # 1 hour and 1 minute
                strip2.fill(green)
            elif i == 2:  # 2 hour and 2 minute
                strip3.fill(green)
            elif i == 3:  # 3 hour and 3 minute
                strip4.fill(green)
            elif i == 4:  # 5 hour and 5 minute
                strip5.fill(green)
        else:  # Not used
            if i == 0:
                strip1.fill(white)
            elif i == 1:
                strip2.fill(white)
            elif i == 2:
                strip3.fill(white)
            elif i == 3:
                strip4.fill(white)
            elif i == 4:
                strip5.fill(white)
        
        # Show the updates
    strip1.show()
    strip2.show()
    strip3.show()
    strip4.show()
    strip5.show()
    utime.sleep(1)
```

### config.json

You will need to update the following config.json file with your Wifi ssid and password, change the date_time_api to your key given by IP Geolocation, and update the time_zone

```json
{
    "ssid": "Open_Internet",
    "ssid_password": "25802580",
    "query_interval_sec": 120,
    "date_time_api": "bf681acbba0d41ce97f85ef3582e7c82",
    "time_zone": "Asia/Shanghai",
}
```
## Enclosure Design

The enclosure was designed in Fusion360. The enclosure consist of three main parts.
The main body which the LED bracket will be inserted which you need to solder all the LED rows and then the insert squares which will diffuse the light from the LEDs.
The STL files are available [here](https://github.com/Guitarman9119/Raspberry-Pi-Pico-/tree/main/Fibonacci%20clock)



<figure><img src="/fib_3D_main.png" alt=""><figcaption></figcaption></figure>

<figure><img src="/fib_3D_insert.png" alt=""><figcaption></figcaption></figure>



The parts does not require any supports when printing.

If anyone decides to recreate this project and comes up with an improved design for the case, please feel free to share it with me. I would love to see what you create!

## Conclusion

The enclosure still needs to be updated as it does not have a back cover yet lol. So future plans is to make a version which will look more like golden ratio, and use LEDs connected on PCB.
