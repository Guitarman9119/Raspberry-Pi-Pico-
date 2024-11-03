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
purple = (0, 255, 0) # Both hours and minutes color
black = (255, 255, 255)      # Off color

# Set brightness for all strips
strip1.brightness(255)
strip2.brightness(255)
strip3.brightness(255)
strip4.brightness(255)
strip5.brightness(255)

# Wi-Fi Configuration
def connect_wifi():
    with open('config.json') as f:
        config = json.load(f)

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(config['ssid'], config['ssid_password'])

    print("Connecting to WiFi...")
    while not wlan.isconnected():
        utime.sleep(1)

    print("Connected to Wi-Fi:", wlan.ifconfig())

# Function to sync time with worldtimeapi.org
def sync_time_with_worldtimeapi_org(rtc):
    TIME_API = "http://worldtimeapi.org/api/timezone/Asia/Shanghai"  # Change to your timezone

    try:
        response = urequests.get(TIME_API)
        if response.status_code == 200:
            json_data = response.json()
            print("Time API Response:", json_data)  # Print the response for debugging
            
            current_time = json_data.get("datetime")
            if current_time is None:
                print("Error: 'datetime' not found in response.")
                return
            
            the_date, the_time = current_time.split("T")
            year, month, mday = [int(x) for x in the_date.split("-")]
            the_time = the_time.split(".")[0]
            hours, minutes, seconds = [int(x) for x in the_time.split(":")]
            
            week_day = json_data.get("day_of_week")
            if week_day is None:
                print("Error: 'day_of_week' not found in response.")
                return
            
            rtc.datetime((year, month, mday, week_day, hours, minutes, seconds, 0))
            response.close()  # Close the response after successful use
        else:
            print("Error fetching time:", response.status_code)
    except Exception as e:
        print("Error fetching time:", e)

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

# Initialize RTC (Real-Time Clock)
rtc = RTC()
connect_wifi()  # Connect to Wi-Fi
sync_time_with_worldtimeapi_org(rtc)  # Sync time from the API

# Main loop to update the NeoPixel LEDs based on the current time
while True:
    current_time = rtc.datetime()
    hours = current_time[4]%12  # Get hours
    minutes = current_time[5]  # Get minutes
    print(hours)
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
                strip1.fill(black)
            elif i == 1:  # 1 minute
                strip2.fill(black)
            elif i == 2:  # 2 minutes
                strip3.fill(blue)
            elif i == 3:  # 3 minutes
                strip4.fill(blue)
            elif i == 4:  # 5 minutes
                strip5.fill(blue)
        elif state[i] == 3:  # Both hour and minute representation
            # Light up the strip corresponding to the Fibonacci value for both
            if i == 0:  # 1 hour and 1 minute
                strip1.fill(purple)
            elif i == 1:  # 1 hour and 1 minute
                strip2.fill(purple)
            elif i == 2:  # 2 hour and 2 minute
                strip3.fill(purple)
            elif i == 3:  # 3 hour and 3 minute
                strip4.fill(purple)
            elif i == 4:  # 5 hour and 5 minute
                strip5.fill(purple)
        else:  # Not used
            if i == 0:
                strip1.fill(black)
            elif i == 1:
                strip2.fill(black)
            elif i == 2:
                strip3.fill(black)
            elif i == 3:
                strip4.fill(black)
            elif i == 4:
                strip5.fill(black)
        
        # Show the updates
    strip1.show()
    strip2.show()
    strip3.show()
    strip4.show()
    strip5.show()
    utime.sleep(1)
    


