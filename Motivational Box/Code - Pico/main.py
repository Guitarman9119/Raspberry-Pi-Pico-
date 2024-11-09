import rp2
import network
import ubinascii
import time
import utime
import socket
import ntptime
import json
from microhttp import WebServer
from neopixel import Neopixel
from machine import Pin, RTC, SPI

# ----------------Begin Network---------------- #
rp2.country('CN')
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print('MAC ' + mac)

ssid = 'ZX_seewo'
psw = 'xwdp2022'

wlan.connect(ssid, psw)

timeout = 10
while timeout > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    timeout -= 1
    time.sleep(1)

wlan_status = wlan.status()

if wlan_status != 3:
    raise RuntimeError('WiFi Connect ERROR')
else:
    print('WiFi Connected')
    status = wlan.ifconfig()
    print('IP ' + status[0])
# ----------------End Network---------------- #

# ----------------Begin File---------------- #
def read_file(filename):
    tmp = ""
    with open(filename, "r") as fp:
        tmp = fp.read()
    return tmp

def write_file(filename,data):
    with open(filename, "w") as fp:
        fp.write(data)
# ----------------End File---------------- #

app = WebServer()

@app.get('/')
def index(request,response):
    response.content_type='text/html'
    return read_file("index.html")

@app.get('/data.json')
def getdata(request,response):
    return read_file("data.json")

@app.post('/new_or_change/')
def new_or_change(request,response):
    tmp = json.loads(read_file("data.json"))
    tmp[int(request.body_param["cid"])]["data"][request.body_param["date"]] = {"note": request.body_param["note"]}
    write_file("data.json", json.dumps(tmp))
    return '{"msg": "ok"}'

@app.post('/del/')
def delrecord(request,response):
    tmp = json.loads(read_file("data.json"))
    del tmp[int(request.body_param["cid"])]["data"][request.body_param["date"]]
    write_file("data.json", json.dumps(tmp))
    return '{"msg": "ok"}'

app.run(blocked=False,port=80)

# ---------------LED and Button---------------#

# Initialize neopixel strip and set colors
numpix = 10
strip = Neopixel(numpix, 0, 0, "GRB")
blank = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 50, 0)
yellow = (255, 150, 0)
green = (0, 255, 0)
blue = (0, 100, 255)
indigo = (100, 0, 90)
violet = (200, 0, 100)
white = (255,255,255)
 
# Set strip brightness
strip.brightness(100)
 
# Define the pin numbers for the buttons
button_pins = [1, 2, 3, 4, 5]
task_names = ['Task 1', 'Task 2', 'Task 3', 'Task 4', 'Task 5']

# Define the LED ranges for each task
task_led_ranges = [[8,9], [6,7], [4,5], [2,3],[0, 1]]
 
# Define the pin objects for the buttons
task_pins = [Pin(pin, Pin.IN, Pin.PULL_DOWN) for pin in button_pins]

# NTP SERVER
NTP_SERVER = "ntp.aliyun.com"

# ----------- Get Time --------------- #
def sync_ntp():
    print("Start Sync NTP Time")
    rtc = RTC()
    try:
        ntptime.NTP_DELTA = 3155644800
        ntptime.host = NTP_SERVER
        ntptime.settime()
        localtime_now=time.time()+8*3600
        localtime_now=time.localtime(localtime_now)
        rtc.datetime((localtime_now[0],localtime_now[1],localtime_now[2],localtime_now[6],localtime_now[3],localtime_now[4],localtime_now[5],localtime_now[7]))
    except Exception as e:
        print("Sync NTP time error",repr(e))
    
    localtime_now=time.localtime()
    
    print("localtime_now","{}-{}-{}".format(localtime_now[0],localtime_now[1],localtime_now[2]))
    return "{}-{}-{}".format(localtime_now[0],localtime_now[1],localtime_now[2])
# ----------- End Get Time --------------- #

print("Start listen button.\n-----------------")

while True:
    for i, pin in enumerate(task_pins):
        if pin.value() == 1:
            print("Button press", i)
            tmp = json.loads(read_file("data.json"))
            tmp[i]["data"][sync_ntp()] = {}
            write_file("data.json", json.dumps(tmp))
            print("----------ok----------")
           # update_leds()
