# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
import adafruit_pyportal

import adafruit_minimqtt.adafruit_minimqtt as MQTT

from adafruit_pyportal import PyPortal


# Setup the PyPortal
# Set up where we'll be fetching data from
DATA_SOURCE = "https://silversaucer.com/album/data"

# There's a few different places we look for data in the photo of the day
IMAGE_LOCATION = ["image_url"]
TITLE_LOCATION = ["artist"]
DATE_LOCATION = ["album"]

# the current working directory (where this file is)
cwd = ("/"+__file__).rsplit('/', 1)[0]
pyportal = PyPortal(url=DATA_SOURCE,
                    json_path=(TITLE_LOCATION, DATE_LOCATION),
                    status_neopixel=board.NEOPIXEL,
                    default_bg=cwd+"/nasa_background.bmp",
                    text_font=cwd+"/fonts/Arial-12.bdf",
                    text_position=((5, 220), (5, 200)),
                    text_color=(0xFFFFFF, 0xFFFFFF),
                    text_maxlen=(50, 50), # cut off characters
                    image_json_path=IMAGE_LOCATION,
                    image_resize=(320, 320),
                    image_position=(0, 0))

### WiFi ###

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# ------------- MQTT Topic Setup ------------- #
mqtt_topic = "albumart"

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
    if message == "Ping!":
        print("New message on topic {0}: {1}".format(topic, message))
        response = None
        try:
            response = pyportal.fetch()
            print("Response is", response)
        except RuntimeError as e:
            print("Some error occurred, retrying! -", e)
        time.sleep(60)




# Connect to WiFi
print("Connecting to WiFi...")
pyportal.network.connect()
print("Connected!")

# Initialize MQTT interface with the esp interface
# pylint: disable=protected-access
MQTT.set_socket(socket, pyportal.network._wifi.esp)

# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(
    broker=secrets["broker"],
    username=secrets["user"],
    password=secrets["pass"],
    is_ssl=False,
)

# Setup the callback methods above
mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_message = message

# Connect the client to the MQTT broker.
mqtt_client.connect()


while True:
    # Poll the message queue
    mqtt_client.loop()

    # Send a new message
    time.sleep(1)
