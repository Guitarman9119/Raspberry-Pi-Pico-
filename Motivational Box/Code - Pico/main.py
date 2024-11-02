import rp2
import network
import ubinascii
import time
import socket
import json
from microhttp import WebServer

# ----------------Begin Network---------------- #
rp2.country('CN')
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print('MAC ' + mac)

ssid = 'ssid'
psw = 'password'

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

@app.get('/bootstrap.min.css')
def staticfile(request,response):
    response.content_type='text/css'
    return read_file("bootstrap.min.css")

@app.get('/bootstrap.min.js')
def staticfile(request,response):
    response.content_type='text/javascript'
    return read_file("bootstrap.min.js")

@app.get('/calendar_yearview_blocks.css')
def staticfile(request,response):
    response.content_type='text/css'
    return read_file("calendar_yearview_blocks.css")

@app.get('/calendar_yearview_blocks.js')
def staticfile(request,response):
    response.content_type='text/javascript'
    return read_file("calendar_yearview_blocks.js")

@app.get('/jquery-3.7.1.min.js')
def staticfile(request,response):
    response.content_type='text/javascript'
    return read_file("jquery-3.7.1.min.js")

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

app.run(blocked=True,port=80)
