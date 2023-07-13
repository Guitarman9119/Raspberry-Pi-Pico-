import utime
from machine import Pin, RTC, SPI
import urequests
import network, json, time
from time import sleep



with open('config.json') as f:
    config = json.load(f)

# Check config.json has updated credentials
if config['ssid'] == 'Enter_Wifi_SSID':
    assert False, ("config.json has not been updated with your unique keys and data")

# Create WiFi connection and turn it on
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Connect to WiFi router
print ("Connecting to WiFi: {}".format( config['ssid'] ) )
wlan.connect( config['ssid'], config['ssid_password'])

# Wait until wifi is connected
while not wlan.isconnected:
    pass

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

    json = response.json()
    current_time = json["datetime"]
    the_date, the_time = current_time.split("T")
    year, month, mday = [int(x) for x in the_date.split("-")]
    the_time = the_time.split(".")[0]
    hours, minutes, seconds = [int(x) for x in the_time.split(":")]

    # We can also fill in these extra nice things
    year_day = json["day_of_year"]
    week_day = json["day_of_week"]
    is_dst = json["dst"]
    response.close()
    rtc.datetime((year, month, mday, week_day, hours, minutes, seconds, 0)) # (year, month, day, weekday, hours, minutes, seconds, subseconds)
    
        
rtc = RTC()
sync_time_with_worldtimeapi_org(rtc)

force_sync_counter = 0


    
if force_sync_counter > 85000: # A little less than a day
    force_sync_counter = 0
    sync_time_with_worldtimeapi_org(rtc, blocking=False)
force_sync_counter = force_sync_counter + 1


# Define the GPIO pins for the LEDs
hour_pins = [Pin(pin, Pin.OUT) for pin in [15,14,13,12,11]]
minute_pins = [Pin(pin, Pin.OUT) for pin in [10,9,8,7,6,5]]
second_pins = [Pin(pin, Pin.OUT) for pin in [16,17,18,19,20,21]]



# Define a function to update the LEDs based on the current time
def update_leds():
    # Get the current time
    Y, M, D, W, H, M, S, SS = rtc.datetime()

    # Convert the hours, minutes, and seconds to binary strings
    hour_binary = '{0:05b}'.format(H)
    minute_binary = '{0:06b}'.format(M)
    second_binary = '{0:06b}'.format(S)
    print("Time:" , H,":",M,":",S)

    # Set the LED states based on the binary values
    for i in range(5):
        hour_pins[i].value(int(hour_binary[i]))
    for i in range(6):
        minute_pins[i].value(int(minute_binary[i]))
    for i in range(6):
        second_pins[i].value(int(second_binary[i]))
        
        
    
# Loop indefinitely, updating the LEDs every second
while True:
    update_leds()
    time.sleep(1)

    

    
    #print(minutes_reverse)
    