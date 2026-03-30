import utime
from machine import Pin, I2C, RTC
import json
import urequests
import network
from ssd1306 import SSD1306_I2C

# ============================
# Load configuration
# ============================
with open('config.json') as f:
    config = json.load(f)

if config['ssid'] == 'Enter_Wifi_SSID':
    raise ValueError("config.json has not been updated with your unique keys and data")

weather_api_key = config['weather_api_key']
city = config['city']
country_code = config['country_code']
date_time_api = config['date_time_api']
timezone = config['time_zone']

# ============================
# Wi-Fi connection
# ============================
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
print("Connecting to WiFi:", config['ssid'])
wlan.connect(config['ssid'], config['ssid_password'])

while not wlan.isconnected():
    utime.sleep(1)
print("Connected to Wi-Fi:", wlan.ifconfig())

# ============================
# RTC
# ============================
rtc = RTC()

def sync_time_with_ip_geolocation_api(rtc):
    try:
        url = f'http://api.ipgeolocation.io/timezone?apiKey={date_time_api}&tz={timezone}'
        response = urequests.get(url)
        data = response.json()
        response.close()

        if 'date_time' in data:
            current_time = data["date_time"]  # e.g. "2025-09-24 07:45:00"
            the_date, the_time = current_time.split(" ")
            year, month, mday = map(int, the_date.split("-"))
            hours, minutes, seconds = map(int, the_time.split(":"))
            week_day = data.get("day_of_week", 0)

            rtc.datetime((year, month, mday, week_day, hours, minutes, seconds, 0))
            print("RTC synced:", rtc.datetime())
            return True
    except Exception as e:
        print("Time sync failed:", e)
    return False

# ============================
# Weather Fetch
# ============================
def fetch_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={weather_api_key}&units=metric"
    try:
        r = urequests.get(url)
        data = r.json()
        r.close()
        return {
            'location': f"{data['name']} - {data['sys']['country']}",
            'description': data['weather'][0]['main'],
            'temperature': data['main']['temp'],
            'pressure': data['main']['pressure'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
        }
    except Exception as e:
        print("Weather fetch failed:", e)
        return None

# ============================
# OLED setup
# ============================
WIDTH = 128
HEIGHT = 64
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
display = SSD1306_I2C(WIDTH, HEIGHT, i2c)

def show_status(msg, line=0):
    """Show temporary status messages on OLED"""
    display.fill(0)
    display.text("NerdCave Clock", 0, 0)
    display.text(msg, 0, 20 + line*12)
    display.show()

# ============================
# Buttons
# ============================
btn_next = Pin(22, Pin.IN, Pin.PULL_DOWN)
btn_prev = Pin(26, Pin.IN, Pin.PULL_DOWN)
current_page = 0
total_pages = 3

def handle_buttons():
    global current_page
    if btn_next.value():
        current_page = (current_page + 1) % total_pages
        utime.sleep_ms(250)
    if btn_prev.value():
        current_page = (current_page - 1) % total_pages
        utime.sleep_ms(250)

# ============================
# LED Binary Clock Pins
# ============================
hour_pins = [Pin(pin, Pin.OUT) for pin in [1, 0]]
hour_pins_ext = [Pin(pin, Pin.OUT) for pin in [11, 4, 3, 2]]
minute_pins = [Pin(pin, Pin.OUT) for pin in [8, 7, 6]]
minute_pins_ext = [Pin(pin, Pin.OUT) for pin in [21, 20, 10, 9]]
second_pins = [Pin(pin, Pin.OUT) for pin in [15, 14, 13]]
second_pins_ext = [Pin(pin, Pin.OUT) for pin in [12, 5, 19, 18]]

def update_leds():
    Y, M, D, W, H, Min, S, SS = rtc.datetime()
    h1, h2 = divmod(H, 10)
    for pin in hour_pins: pin.value(0)
    for pin in hour_pins_ext: pin.value(0)
    if h1 == 2: hour_pins[0].value(1)
    elif h1 == 1: hour_pins[1].value(1)
    for i in range(4):
        hour_pins_ext[i].value((h2 >> (3 - i)) & 1)
    m1, m2 = divmod(Min, 10)
    for i in range(3):
        minute_pins[i].value((m1 >> (2 - i)) & 1)
    for i in range(4):
        minute_pins_ext[i].value((m2 >> (3 - i)) & 1)
    s1, s2 = divmod(S, 10)
    for i in range(3):
        second_pins[i].value((s1 >> (2 - i)) & 1)
    for i in range(4):
        second_pins_ext[i].value((s2 >> (3 - i)) & 1)

# ============================
# OLED Pages
# ============================
def display_time_date():
    Y, M, D, W, H, Min, S, SS = rtc.datetime()
    display.fill(0)
    display.text("NerdCave Clock", 0, 0)
    display.text(f"{D:02}-{M:02}-{Y}", 0, 20)
    display.text(f"{H:02}:{Min:02}:{S:02}", 0, 35)
    display.show()

def display_weather_basic(weather):
    display.fill(0)
    display.text("Weather:", 0, 0)
    display.text(weather['location'], 0, 12)
    display.text(f"T:{weather['temperature']}C", 0, 24)
    display.text(weather['description'], 0, 36)
    display.text(f"H:{weather['humidity']}%", 0, 48)
    display.show()

def display_weather_extended(weather):
    display.fill(0)
    display.text("Weather Ext:", 0, 0)
    display.text(f"Pressure:{weather['pressure']}", 0, 16)
    display.text(f"Wind:{weather['wind_speed']}m/s", 0, 32)
    display.text(f"Temp:{weather['temperature']}C", 0, 48)
    display.show()

# ============================
# Startup status
# ============================
show_status("WiFi Connected")

weather_data = fetch_weather()
if weather_data:
    show_status("Weather Sync OK")
else:
    show_status("Weather Error")

if sync_time_with_ip_geolocation_api(rtc):
    show_status("Time Sync OK", line=1)
else:
    show_status("Time Sync FAIL", line=1)

utime.sleep(2)  # Show status for 2s

# ============================
# Main Loop
# ============================
last_weather_update = utime.time()
last_time_sync = utime.time()
last_tick = utime.ticks_ms()

while True:
    if utime.ticks_diff(utime.ticks_ms(), last_tick) >= 1000:
        last_tick = utime.ticks_ms()

        update_leds()
        handle_buttons()

        if current_page == 0:
            display_time_date()
        elif current_page == 1 and weather_data:
            display_weather_basic(weather_data)
        elif current_page == 2 and weather_data:
            display_weather_extended(weather_data)

        if utime.time() - last_weather_update > 600:
            weather_data = fetch_weather()
            last_weather_update = utime.time()

        if utime.time() - last_time_sync > 600:
            sync_time_with_ip_geolocation_api(rtc)
            last_time_sync = utime.time()
