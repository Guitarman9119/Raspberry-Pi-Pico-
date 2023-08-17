import os
import json
import utime
from neopixel import Neopixel
from machine import Pin, RTC, SPI
import urequests
import network, json, time
from time import sleep
import binascii
import os

# Initialize neopixel strip and set colors
numpix = 10
strip = Neopixel(numpix, 0, 0, "GRB")
blank = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
 
# Set strip brightness
strip.brightness(100)
 
# Define the pin numbers for the buttons
button_pins = [1, 2, 3, 4, 5]
task_names = ['Task 1', 'Task 2', 'Task 3', 'Task 4', 'Task 5']

# Define the LED ranges for each task
task_led_ranges = [[8,9], [6,7], [4,5], [2,3],[0, 1]]
 
# Define the pin objects for the buttons
task_pins = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in button_pins]

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

print("Internet connected")

def file_or_dir_exists(filename):
    try:
        os.stat(filename)
        return True
    except OSError:
        return False
 
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

Y, M, D, W, H, _, _, _ = rtc.datetime()

def get_sha_git():
    token = "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"
    repo = 'Guitarman9119/motivational_box'
    path = 'static/db.json'-

    r = urequests.get(
        f'https://api.github.com/repos/{repo}/contents/{path}',
        headers={
            'Authorization': f'Token {token}',
            'User-Agent': 'Pico User Agent 1.0'
        }
    )

    #print(r.status_code)
    #print(r.text)
    js = r.json()
    #print(js)
    return js['sha']


def update_git():
    token = "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"
    repo = 'Guitarman9119/motivational_box'
    path = 'static/db.json'

    # Read the data from the file
    with open("db.json", "r") as file:
        data = file.read()

    # Encode the data using Base64
    encoded_data = binascii.b2a_base64(data.encode())

    sha = get_sha_git()

    print('encoded data',encoded_data)
    r = urequests.put(
        f'https://api.github.com/repos/{repo}/contents/{path}',
        headers={
            'Authorization': f'Token {token}',
            'User-Agent': 'Pico User Agent 1.0'
        },
        json={
            "message": "update daily tasks db.json",
            "content": encoded_data,
            "branch": "main",
            'sha': sha
        }
    )

    #print(r.status_code)
    #print(r.text)
    #print(r.json())
    



def create_db(db_path):
    if not file_or_dir_exists(db_path):
        with open(db_path, 'w') as f:
            json.dump({}, f)
 
def set_task_completed(task_name, db_path):
    rtc = RTC()
    sync_time_with_worldtimeapi_org(rtc)
    create_db(db_path)

    Y, M, D, W, H, _, _, _ = rtc.datetime()
    day_month_year = f"{Y}/{M}/{D}"

    print("Task completed", task_name, day_month_year) # Add print
 
    db = json.load(open(db_path, 'r'))
 
    if day_month_year not in db:
        db[day_month_year] = {}
 
    db[day_month_year][task_name] = True
 
    with open(db_path, 'w') as f:
        json.dump(db, f)
 
def get_completed_tasks(db_path):
    rtc = RTC()
    create_db(db_path)
    db = json.load(open(db_path, 'r'))
 
    Y, M, D, W, H, _, _, _ = rtc.datetime()
    day_month_year = f"{Y}/{M}/{D}"
 
    if day_month_year not in db: return []
 
    return [task for task in db[day_month_year] if db[day_month_year][task] == True]
 
def update_leds(task_status):
    print('update_leds',task_status)
    # Clear all LEDs to blank (black) color
    for i in range(numpix):
        strip.set_pixel(i, red)
 
    # Set LED colors based on task status
    for i, status in enumerate(task_status):
        led_range = task_led_ranges[i]
        color = green if status else red
        for j in range(led_range[0], led_range[1] + 1):
            strip.set_pixel(j, color)
 
    strip.show()  # Update the neopixel LEDs
    update_git()
    print("Done")
    
    
    

    
def update_tasks(task_names,db_path):   
    task_status = [False for _ in task_names]
    for completed_task in get_completed_tasks(db_path):
        # find index of completed task in task_names
        try:
            task_index = task_names.index(completed_task)
            task_status[task_index] = True
        
        except:
            print("Invalid task found", completed_task)
    # Set LEDS to task_status 
    update_leds(task_status)
   
 
def check_button_pressed(task_names,db_path):
    for i, pin in enumerate(task_pins):
        if pin.value() == 0:
            task_name = task_names[i]
            if task_name not in get_completed_tasks(db_path):
                set_task_completed(task_name, db_path)
                print(f"{task_name} completed")
                update_tasks(task_names,db_path) # Add update_tasks hierso om LED te change
 
def update_loop(task_names,db_path):
    # 12 pm tomorrow
    print(rtc.datetime())
    Y, M, D, W, H, _, _, _ = rtc.datetime()
    year_s = Y*365*24*60*60
    month_s = M*30*24*60*60
    day_s = (D+1)*24*60*60 # next day
    hour_s = 12*60*60 # 12 pm
    next_update_s = year_s + month_s+day_s+hour_s


    
 
    while True:
        Y, M, D, W, H, _, _, _ = rtc.datetime()
        year_s = Y*365*24*60*60
        month_s = M*30*24*60*60
        day_s = D*24*60*60
        hour_s = H*60*60
        current_s = year_s+month_s+day_s+hour_s

        
        # check button press
        #print("current_s:", current_s)
        #print("next_update_s",next_update_s)
        check_button_pressed(task_names,db_path)
        if current_s > next_update_s:
            
            update_tasks(task_names,db_path)

            Y, M, D, W, H, _, _, _ = rtc.datetime()
            year_s = Y*365*24*60*60
            month_s = M*30*24*60*60
            day_s = (D+1)*24*60*60 # next day
            hour_s = 12*60*60 # 12 pm 
            next_update_s = year_s + month_s+day_s+hour_s
            update_git()

 
# Get the current working directory
cwd = os.getcwd()
db_path = cwd + '/db.json' 
 

 
 
if __name__ == '__main__':
    update_tasks(task_names,db_path)
    update_loop(task_names,db_path) # Loop forever