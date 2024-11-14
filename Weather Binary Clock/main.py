import utime
from machine import Pin, I2C, RTC
import json
import urequests
import network
from ssd1306 import SSD1306_I2C

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

# Create WiFi connection and turn it on
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Connect to WiFi router
print("Connecting to WiFi:", config['ssid'])
wlan.connect(config['ssid'], config['ssid_password'])

# Wait until WiFi is connected
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


# Function to fetch weather data
def fetch_weather():
    open_weather_map_url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={weather_api_key}&units=metric"
    print("Fetching weather data from:", open_weather_map_url)
    
    try:
        weather_data = urequests.get(open_weather_map_url)
        if weather_data.status_code == 200:
            weather_json = weather_data.json()
            print("Weather Data:", weather_json)

            # Extracting relevant weather information
            return {
                'location': f"{weather_json['name']} - {weather_json['sys']['country']}",
                'description': weather_json['weather'][0]['main'],
                'temperature': weather_json['main']['temp'],
                'pressure': weather_json['main']['pressure'],
                'humidity': weather_json['main']['humidity'],
                'wind_speed': weather_json['wind']['speed'],
            }
        else:
            print("Weather API Error:", weather_data.status_code, weather_data.text)
    except Exception as e:
        print("An error occurred while fetching weather data:", str(e))
    return None

# Initialize RTC and sync time
rtc = RTC()
sync_time_with_ip_geolocation_api(rtc)

# Define the GPIO pins for the LEDs
hour_pins = [Pin(pin, Pin.OUT) for pin in [1, 0]]  # 2 bits for hours (0-1)
hour_pins_ext = [Pin(pin, Pin.OUT) for pin in [11, 4, 3, 2]]  # 4 bits for hours (2-5)
minute_pins = [Pin(pin, Pin.OUT) for pin in [8, 7, 6]]  # 3 bits for first minute (0-7)
minute_pins_ext = [Pin(pin, Pin.OUT) for pin in [21, 20, 10, 9]]  # 4 bits for second minute (0-9)
second_pins = [Pin(pin, Pin.OUT) for pin in [15, 14, 13]]  # 3 bits for first second (0-7)
second_pins_ext = [Pin(pin, Pin.OUT) for pin in [12, 5, 19, 18]]  # 4 bits for second second (0-9)

# Function to update the LEDs based on the current time
def update_leds():
    Y, M, D, W, H, Min, S, SS = rtc.datetime()
    print("Time:", H, ":", Min, ":", S)

    hour_msb = H // 10
    hour_lsb = H % 10
    minute_msb = Min // 10
    minute_lsb = Min % 10
    second_msb = S // 10
    second_lsb = S % 10

    # Update hour pins
    hour_pins[0].value(hour_msb)
    hour_pins[1].value(hour_lsb)
    for i in range(4):
        hour_pins_ext[i].value((hour_lsb >> (3 - i)) & 1)

    # Update minute pins
    for i in range(3):
        minute_pins[i].value((minute_msb >> (2 - i)) & 1)
    for i in range(4):
        minute_pins_ext[i].value((minute_lsb >> (3 - i)) & 1)

    # Update second pins
    for i in range(3):
        second_pins[i].value((second_msb >> (2 - i)) & 1)
    for i in range(4):
        second_pins_ext[i].value((second_lsb >> (3 - i)) & 1)

# OLED display dimensions
WIDTH = 128
HEIGHT = 64

# Initialize I2C and OLED display
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
display = SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Function to update the OLED display with weather data
def update_display(weather_data):
    display.fill(0)  # Clear the display
    display.text('NerdCave Clock', 0, 0)
    display.text('Weather Data', 0, 10)
    display.text(weather_data['location'], 0, 20)
    display.text(f'Temp: {weather_data["temperature"]} C', 0, 30)
    display.text(f'Desc: {weather_data["description"]}', 0, 40)
    display.text(f'Humidity: {weather_data["humidity"]}%', 0, 50)
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
    
    utime.sleep(1)

