import utime
from machine import I2C, Pin, RTC
import json
import network
import urequests
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

# LCD Setup
I2C_ADDR = 63
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

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
        print("Still trying to connect...")

    print("Connected to Wi-Fi:", wlan.ifconfig())

# Function to sync time with IP Geolocation API
def sync_time_with_ip_geolocation_api(rtc):
    with open('config.json') as f:
        config = json.load(f)

    date_time_api = config['date_time_api']
    timezone = config['time_zone']

    url = f'http://api.ipgeolocation.io/timezone?apiKey={date_time_api}&tz={timezone}'
    response = urequests.get(url)
    data = response.json()

    print("API Response:", data)

    if 'date_time' in data:
        current_time = data["date_time"]
        print("Current Time String:", current_time)

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

# Function to display time on LCD
def display_time(rtc):
    previous_time_str = ""
    previous_date_str = ""

    while True:
        current_time = rtc.datetime()  # Get current time
        # Format the time string
        time_str = f"{current_time[4]:02}:{current_time[5]:02}:{current_time[6]:02}"  # HH:MM:SS
        date_str = f"{current_time[2]:02}/{current_time[1]:02}/{current_time[0]}"  # DD/MM/YYYY


        # Update only if the time or date has changed
        if time_str != previous_time_str:
            lcd.move_to(0, 0)  # Move cursor to the first row
            lcd.putstr(time_str)  # Display time without padding

        if date_str != previous_date_str:
            lcd.move_to(0, 1)  # Move cursor to the second row
            lcd.putstr(date_str)  # Display date without padding

        # Save the current time and date for the next comparison
        previous_time_str = time_str
        previous_date_str = date_str

        utime.sleep(1)  # Update every second

# Main program flow
def main():
    connect_wifi()
    rtc = RTC()
    sync_time_with_ip_geolocation_api(rtc)

    # Start displaying time
    display_time(rtc)

############################ WEB SERVER #######################
def read_file(filename):
    tmp = ""
    with open(filename, "r") as fp:
        tmp = fp.read()
    return tmp

app = WebServer()

@app.get('/')
def index(request,response):
    response.content_type='text/html'
    return read_file("index.html")

@app.post('/change_time/')
def new_or_change(request,response):
    set_hour = request.body_param["hour"]
    set_minute = request.body_param["minute"]
    set_second = request.body_param["seconds"]
    return '{"msg": "ok"}'

app.run(blocked=False,port=80)

###################### END WEB SERVER ####################

main()