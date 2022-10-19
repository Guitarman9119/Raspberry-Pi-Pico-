#Example 1 - Control individual LED

from neopixel import Neopixel
import utime
import random

from micropython_youtube_api import YoutubeAPI
import network, json, time

numpix = 256
strip = Neopixel(numpix, 0, 28, "GRB")

red = (255, 0, 0)

red = (255, 0, 0)
orange = (255, 50, 0)
yellow = (255, 100, 0)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 255)
indigo = (100, 0, 90)
violet = (200, 0, 100)
colors_rgb = [red, orange, yellow, green, blue, indigo, violet]

delay = 0.5
strip.brightness(42)
blank = (0,0,0)

NUMBERS = [[
  0b00000000,
  0b11100000,
  0b10100000,
  0b10100000,
  0b10100000,
  0b11100000,
  0b00000000,
  0b00000000
],[
  0b00000000,
  0b11000000,
  0b01000000,
  0b01000000,
  0b01000000,
  0b11100000,
  0b00000000,
  0b00000000
],[
  0b00000000,
  0b11100000,
  0b00100000,
  0b11100000,
  0b10000000,
  0b11100000,
  0b00000000,
  0b00000000
],[
  0b00000000,
  0b11100000,
  0b00100000,
  0b11100000,
  0b00100000,
  0b11100000,
  0b00000000,
  0b00000000
],[
  0b00000000,
  0b10100000,
  0b10100000,
  0b11100000,
  0b00100000,
  0b00100000,
  0b00000000,
  0b00000000
],[
  0b00000000,
  0b11100000,
  0b10000000,
  0b11100000,
  0b00100000,
  0b11100000,
  0b00000000,
  0b00000000
],[
  0b00000000,
  0b11100000,
  0b10000000,
  0b11100000,
  0b10100000,
  0b11100000,
  0b00000000,
  0b00000000
],[
  0b00000000,
  0b11100000,
  0b00100000,
  0b00100000,
  0b00100000,
  0b00100000,
  0b00000000,
  0b00000000
],[
  0b00000000,
  0b11100000,
  0b10100000,
  0b11100000,
  0b10100000,
  0b11100000,
  0b00000000,
  0b00000000
],[
  0b00000000,
  0b11100000,
  0b10100000,
  0b11100000,
  0b00100000,
  0b11100000,
  0b00000000,
  0b00000000
]
           ]

YOUTUBE_LOGO = [[
  0b00000000,
  0b01111110,
  0b11101111,
  0b11100111,
  0b11100111,
  0b11101111,
  0b01111110,
  0b00000000
],[
  0b00000000,
  0b00000000,
  0b00010000,
  0b00011000,
  0b00011000,
  0b00010000,
  0b00000000,
  0b00000000
]]


def generate_remap():
    remap = []
    for i in range(0,32):
        for j in range(0,8):
            if i%2 == 0:
                remap.append(i*8+j)
            else:
                remap.append(8-j-1 + i*8)
    return remap
    
def get_index(x,y):
    ind = x*8+y
    remap = generate_remap()
    return remap[ind]

# NUMBERS = [[
#   0b00000000,
#   0b11100000,
#   0b10100000,
#   0b10100000,
#   0b10100000,
#   0b11100000,
#   0b00000000,
#   0b00000000
# ],[
#   0b00000000,
#   0b11000000,
#   0b01000000,
#   0b01000000,
#   0b01000000,
#   0b01000000,
#   0b11100000,
#   0b00000000
# ]]

def set_pixel(x,y, color): 
    strip.set_pixel(get_index(x,y),color)

def draw_image(img, color, offset=0):
    for i in range(0,len(img)):
        for x in range(0,8):
            row = img[i]
            x_left = 8-x-1 # count from left
            is_set = ( row & (1 << x_left) ) > 0
            if is_set:
                set_pixel(x+offset,i, color)
            #print(x,i,is_set)

def get_pos_nums(num):
    pos_nums = []
    while num != 0:
        pos_nums.append(num % 10)
        num = num // 10
    return pos_nums

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

# Create an instance of the YoutubeApi
with YoutubeAPI( config["channelid"], config["appkeyid"], config["query_interval_sec"] ) as data:

    # Read the data every X seconds
    update_interval = 5
    update_stats_time = time.time() - 10

#draw_image(NUMBERS[8], offset=0, color=yellow)
draw_image(YOUTUBE_LOGO[0],red, offset=0)
draw_image(YOUTUBE_LOGO[1],white, offset=0)
#draw_image(NUMBERS[3], offset=4)
#draw_image(NUMBERS[5], offset=10)

# def set_pixel(x,y):
#     ind = get_index(x,y)
#     print(ind)
#     strip.set_pixel(ind, (255,0,0) )




#strip.set_pixel(random.randint(0, numpix-1), colors_rgb[random.randint(0, len(colors_rgb)-1)])
#strip.set_pixel(random.randint(0, numpix-1), colors_rgb[random.randint(0, len(colors_rgb)-1)])
#strip.set_pixel(random.randint(0, numpix-1), colors_rgb[random.randint(0, len(colors_rgb)-1)])
#strip.set_pixel(random.randint(0, numpix-1), colors_rgb[random.randint(0, len(colors_rgb)-1)])
#strip.set_pixel(random.randint(0, numpix-1), colors_rgb[random.randint(0, len(colors_rgb)-1)])
strip.show()
utime.sleep(delay)

while True:
    if update_stats_time < time.time():
        update_stats_time = time.time() + update_interval
        print ("Subs {}".format( data.subs ) )
        print ("Views {}".format( data.views ) )
        print ("Videos {}".format( data.videos ) )
        subsribers = int(data.subs)
        
        


    subs = get_pos_nums(subsribers)
    
    new_list = [subs[len(subs) - i]
                for i in range(1, len(subs)+1)]
    

    
    strip.clear()
    draw_image(YOUTUBE_LOGO[0],red, offset=0)
    draw_image(YOUTUBE_LOGO[1],white, offset=0)
    draw_image(NUMBERS[new_list[0]], red,offset=10)
    draw_image(NUMBERS[new_list[1]], red,offset=16)
    draw_image(NUMBERS[new_list[2]], red,offset=22)
    draw_image(NUMBERS[new_list[3]], red,offset=28)
    strip.show()






    
    
        
          
