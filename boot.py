# boot.py -- run on boot-up

# Complete project details at https://RandomNerdTutorials.com

import time
import webrepl
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None) # turn off vendor O/S debugging messages
import gc
gc.collect()

import config # use config.py to set up sensitive info
ssid = config.my_ssid
my_ssid_password = config.my_ssid_password
mqtt_server = config.my_mqtt_server
#EXAMPLE IP ADDRESS
#mqtt_server = '192.168.1.144'
# global client_id, topic_sub, topic_pub
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'notification'
topic_pub = b'hello'

last_message = 0
message_interval = 60
counter = 0

# station = network.WLAN(network.STA_IF)
# print(station.ifconfig())
# # station.disconnect()
# # station.active(False)

# if station.isconnected() == False:
#     station.active(True)
#     station.connect(ssid, my_ssid_password)
    
    

#     while station.isconnected() == False:
#         pass

# print('Connection successful')

from wifi_setup.wifi_setup import WiFiSetup
ws = WiFiSetup("ding-5cd80b1")
sta = ws.connect_or_setup()

mac = ubinascii.hexlify(sta.config('mac'),':').decode()

client_id = f'ESP8266:{client_id.decode("utf-8")}-{mac}'


webrepl.start()
