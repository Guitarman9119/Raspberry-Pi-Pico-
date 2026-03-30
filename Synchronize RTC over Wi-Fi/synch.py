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
    


rtc = RTC()

sync_time_with_ip_geolocation_api(rtc)