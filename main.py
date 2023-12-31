import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp

import config

def sub_cb(topic, msg):
  print((topic, msg))
  if topic == b'notification' and msg == b'received':
    print('ESP received hello message')

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub

  client = MQTTClient(client_id,
                      mqtt_server,
                      user=config.my_mqtt_user,
                      password=config.my_mqtt_password,
                      ssl=True,
                      ssl_params={})# "cert_reqs":"ssl.CERT_REQUIRED"})
  client.set_callback(sub_cb)
  print(client.connect())
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

while True:
  try:
    client.check_msg()
    if (time.time() - last_message) > message_interval:
      msg = b'Hello #%d' % counter
      client.publish(topic_pub, msg)
      last_message = time.time()
      counter += 1
  except OSError as e:
    restart_and_reconnect()
  except:
    
    client.disconnect()

