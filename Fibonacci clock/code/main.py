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
    




