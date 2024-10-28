import utime
from machine import Pin, I2C, RTC
from pico_i2c_lcd import I2cLcd
import urequests
import network
import json

# Load configuration
with open('config.json') as f:
    config = json.load(f)

# Check config.json has updated credentials
if config['ssid'] == 'Enter_Wifi_SSID':
    assert False, ("config.json has not been updated with your unique keys and data")

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
def sync_time_with_worldtimeapi_org(rtc):
    TIME_API = "http://worldtimeapi.org/api/timezone/Asia/Shanghai"

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

# Setup LCD I2C and initialize
I2C_ADDR = 63
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
lcd.backlight_on()

# Initialize RTC
rtc = RTC()
sync_time_with_worldtimeapi_org(rtc)

# Initialize Buzzer
buzzer = machine.PWM(machine.Pin(15))

def tone(pin, frequency, duration):
    pin.freq(frequency)
    pin.duty_u16(30000)
    utime.sleep_ms(duration)
    pin.duty_u16(0)

# Button pins for alarm setting
Button_pins = [11, 12, 13, 14]
set_hour = 0  # Initially set to a valid hour
set_minute = 0  # Initially set to a valid minute
Button = []

for x in range(4):
    Button.append(Pin(Button_pins[x], Pin.IN, Pin.PULL_UP))

def format_time(value):
    """Format the hour or minute to be two digits."""
    return '0' + str(value) if value < 10 else str(value)

def set_alarm():
    global set_hour, set_minute
    lcd.clear()
    
    current_setting = "hour"  # Start with hour
    while True:
        lcd.move_to(0, 0)
        lcd.putstr(f"Hour: {format_time(set_hour)}")  # Display hour in the first row
        lcd.move_to(0, 1)
        lcd.putstr(f"Minute: {format_time(set_minute)}")  # Display minute in the second row
        
        # Button checks
        if Button[0].value() == 0:  # Confirm setting
            print("Alarm set to:", set_hour, ":", set_minute)
            utime.sleep(0.5)  # Debounce delay
            break
        
        if Button[1].value() == 0:  # Increment
            if current_setting == "hour":
                set_hour = (set_hour + 1) % 24
                utime.sleep(0.2)  # Debounce delay
        
        if Button[2].value() == 0:  # Decrement
            if current_setting == "hour":
                set_hour = (set_hour - 1) % 24
            else:
                set_minute = (set_minute - 1) % 60
            utime.sleep(0.2)  # Debounce delay
        
        if Button[3].value() == 0:  # Switch setting
            current_setting = "minute" if current_setting == "hour" else "hour"
            utime.sleep(0.2)  # Debounce delay

        # Additional delay to prevent rapid switching
        utime.sleep(0.1)

def check_alarm():
    global set_hour, set_minute
    Y, M, D, W, H, Min, S, SS = rtc.datetime()
    if set_hour == H and set_minute == Min:  # Check only hour and minute
        while True:
            lcd.clear()
            lcd.move_to(4, 0)
            lcd.putstr("Wake Up!")
            tone(buzzer, 440, 250)
            utime.sleep_ms(500)
            if Button[3].value() == 0:  # Press any button to stop alarm
                buzzer.high()
                break

utime.sleep(1)
lcd.move_to(0, 0)
lcd.putstr("Pico Alarm Clock")
lcd.move_to(0, 1)
lcd.putstr("  Version 1.0   ")
utime.sleep(4)
lcd.clear()

while True:
    # Use RTC to get the current time
    Y, M, D, W, H, Min, S, SS = rtc.datetime()
    
    # Format time and date
    time_str = f"{H:02}:{Min:02}:{S:02}"
    date_str = f"{D:02}/{M:02}/{Y}"

    lcd.move_to(0, 0)
    lcd.putstr("Time: " + time_str)
    lcd.move_to(0, 1)
    lcd.putstr("Date: " + date_str)
    
    if Button[0].value() == 0:  # Button pressed for setting the alarm
        utime.sleep(0.1)  # Debounce
        print("Set Alarm")
        utime.sleep(1)
        set_alarm()
    
    check_alarm()

    utime.sleep(1)  # Update every second
