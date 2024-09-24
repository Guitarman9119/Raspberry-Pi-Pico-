import utime
from machine import Pin, I2C, RTC
from ssd1306 import SSD1306_I2C
import urequests
import network
import json
import time



# Load configuration
with open('config.json') as f:
    config = json.load(f)

# Check config.json has updated credentials
if config['ssid'] == 'Enter_Wifi_SSID':
    assert False, ("config.json has not been updated with your unique keys and data")

# Your OpenWeatherMap API details
weather_api_key = config['weather_api_key']
city = config['city']
country_code = config['country_code']

# Create WiFi connection and turn it on
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Connect to WiFi router
print("Connecting to WiFi: {}".format(config['ssid']))
wlan.connect(config['ssid'], config['ssid_password'])

# Wait until WiFi is connected
while not wlan.isconnected():
    utime.sleep(1)

print("Connected to Wi-Fi:", wlan.ifconfig())

# Function to sync time with worldtimeapi.org
def sync_time_with_worldtimeapi_org(rtc, blocking=True):
    TIME_API = "http://worldtimeapi.org/api/timezone/Asia/Shanghai"

    response = None
    while True:
        try:
            response = urequests.get(TIME_API)
            break
        except:
            if blocking:
                response.close()
                continue
            else:
                response.close()
                return

    json_data = response.json()
    current_time = json_data["datetime"]
    the_date, the_time = current_time.split("T")
    year, month, mday = [int(x) for x in the_date.split("-")]
    the_time = the_time.split(".")[0]
    hours, minutes, seconds = [int(x) for x in the_time.split(":")]

    week_day = json_data["day_of_week"]
    response.close()
    rtc.datetime((year, month, mday, week_day, hours, minutes, seconds, 0))

# Function to fetch weather data
def fetch_weather():
    open_weather_map_url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={weather_api_key}&units=metric"
    try:
        print("Fetching weather data from:", open_weather_map_url)
        weather_data = urequests.get(open_weather_map_url)

        if weather_data.status_code == 200:
            weather_json = weather_data.json()
            print("Weather Data:", weather_json)

            # Extracting relevant weather information
            return {
                'location': weather_json.get('name') + ' - ' + weather_json.get('sys').get('country'),
                'description': weather_json.get('weather')[0].get('main'),
                'temperature': weather_json.get('main').get('temp'),
                'pressure': weather_json.get('main').get('pressure'),
                'humidity': weather_json.get('main').get('humidity'),
                'wind_speed': weather_json.get('wind').get('speed'),
            }
        else:
            print("Weather API Error:", weather_data.status_code, weather_data.text)
    except Exception as e:
        print("An error occurred while fetching weather data:", str(e))
    return None

rtc = RTC()
sync_time_with_worldtimeapi_org(rtc)

# Define the GPIO pins for the LEDs
hour_pins = [Pin(pin, Pin.OUT) for pin in [0, 1]]  # 2 bits for hours (0-1)
hour_pins_ext = [Pin(pin, Pin.OUT) for pin in [2, 3, 4, 5]]  # 4 bits for hours (2-5)
minute_pins = [Pin(pin, Pin.OUT) for pin in [6, 7, 8]]  # 3 bits for first minute (0-7)
minute_pins_ext = [Pin(pin, Pin.OUT) for pin in [9, 10, 11, 12]]  # 4 bits for second minute (0-9)
second_pins = [Pin(pin, Pin.OUT) for pin in [13, 14, 15]]  # 3 bits for first second (0-7)
second_pins_ext = [Pin(pin, Pin.OUT) for pin in [16, 17, 18, 19]]  # 4 bits for second second (0-9)

# Function to update the LEDs based on the current time
def update_leds():
    Y, M, D, W, H, Min, S, SS = rtc.datetime()  # Changed M to Min to avoid conflict
    print("Time:", H, ":", Min, ":", S)

    hour_msb = H // 10
    hour_lsb = H % 10
    minute_msb = Min // 10
    minute_lsb = Min % 10
    second_msb = S // 10
    second_lsb = S % 10

    hour_msb_binary = '{0:02b}'.format(hour_msb)
    hour_lsb_binary = '{0:04b}'.format(hour_lsb)
    hour_pins[0].value(int(hour_msb_binary[0]))
    hour_pins[1].value(int(hour_msb_binary[1]))
    for i in range(4):
        hour_pins_ext[i].value(int(hour_lsb_binary[i]))

    minute_msb_binary = '{0:03b}'.format(minute_msb)
    minute_lsb_binary = '{0:04b}'.format(minute_lsb)
    for i in range(3):
        minute_pins[i].value(int(minute_msb_binary[i]))
    for i in range(4):
        minute_pins_ext[i].value(int(minute_lsb_binary[i]))

    second_msb_binary = '{0:03b}'.format(second_msb)
    second_lsb_binary = '{0:04b}'.format(second_lsb)
    for i in range(3):
        second_pins[i].value(int(second_msb_binary[i]))
    for i in range(4):
        second_pins_ext[i].value(int(second_lsb_binary[i]))


# OLED display dimensions
WIDTH = 128
HEIGHT = 64
# Initialize I2C and OLED display
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
display = SSD1306_I2C(WIDTH, HEIGHT, i2c)


# Function to update the OLED display with weather data
def update_display(weather_data):
    display.fill(0)  # Clear the display
    display.text('{}'.format(weather_data['location']), 0, 0)
    display.text('Temp: {} C'.format(weather_data['temperature']), 0, 10)
    display.text('Desc: {}'.format(weather_data['description']), 0, 20)
    display.show()  # Update the display

# Fetch initial weather data
weather_data = fetch_weather()
if weather_data:
    update_display(weather_data)

# Loop indefinitely, updating the LEDs every second and checking for weather updates every 10 minutes
last_weather_update = utime.time()
while True:
    update_leds()
    
    # Check if 10 minutes have passed
    if utime.time() - last_weather_update > 600:  # 600 seconds = 10 minutes
        weather_data = fetch_weather()
        if weather_data:
            update_display(weather_data)  # Update the display with new weather data
            last_weather_update = utime.time()  # Reset the timer
    
    time.sleep(1)
