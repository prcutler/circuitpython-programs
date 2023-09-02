import os
import ssl
import time

import adafruit_minimqtt.adafruit_minimqtt as MQTT
import displayio
import socketpool
import wifi
from adafruit_matrixportal.matrix import Matrix

wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
pool = socketpool.SocketPool(wifi.radio)
# requests = adafruit_requests.Session(pool, ssl.create_default_context())
ssl_context = ssl.create_default_context()

displayio.release_displays()
matrix = Matrix(width=64, height=32, bit_depth=6)
display = matrix.display

# ------------- MQTT Topic Setup ------------- #
mqtt_topic = "prcutler/feeds/audio"


### Code ###
# Define callback methods which are called when events occur
# pylint: disable=unused-argument, redefined-outer-name
def connected(client, userdata, flags, rc):
    # This function will be called when the client is connected
    # successfully to the broker.
    print("Subscribing to %s" % (mqtt_topic))
    client.subscribe(mqtt_topic)


def disconnected(client, userdata, rc):
    # This method is called when the client is disconnected
    print("Disconnected from MQTT Broker!")


def message(client, topic, message):
    """Method callled when a client's subscribed feed has a new
    value.
    :param str topic: The topic of the feed with a new value.
    :param str message: The new value
    """
    print(topic, message)


# Initialize MQTT interface with the esp interface
# pylint: disable=protected-access
# MQTT.set_socket(socket, pyportal.network._wifi.esp)

# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(
    broker="io.adafruit.com",
    port=8883,
    username=os.getenv('aio_username'),
    password=os.getenv('aio_key'),
    ssl_context=ssl_context,
    socket_pool=pool,
    is_ssl=True,
)

# Setup the callback methods above
mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_message = message

ssl_context = ssl.create_default_context()

# Connect the client to the MQTT broker.
mqtt_client.connect()


while True:
    # Poll the message queue
    try:
        mqtt_client.loop()

    except RuntimeError or ConnectionError:
        time.sleep(10)
        mqtt_client.connect()
        mqtt_client.loop()

    # Send a new message
    time.sleep(5)