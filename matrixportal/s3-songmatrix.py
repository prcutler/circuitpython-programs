# SPDX-FileCopyrightText: 2020 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# This example implements a simple two line scroller using
# Adafruit_CircuitPython_Display_Text. Each line has its own color
# and it is possible to modify the example to use other fonts and non-standard
# characters.

import adafruit_display_text.label
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio

import socketpool
import ssl
import wifi
import adafruit_connection_manager
import adafruit_requests
import os
import time
import json
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from adafruit_io.adafruit_io import IO_MQTT, IO_HTTP
from adafruit_minimqtt.adafruit_minimqtt import MMQTTException
import adafruit_requests
import asyncio


# wifi.radio.connect(ssid=os.getenv('CIRCUITPY_WIFI_SSID'),
#                   password=os.getenv('CIRCUITPY_WIFI_PASSWORD'))

# WIFI SETUP
def connect_wifi_mqtt():
    if wifi:
        while not wifi.radio.connected:
            print("Connecting to wifi...")
            wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))
            time.sleep(1)
    else:
        while not esp.is_connected:
            print("Connecting to wifi...")
            esp.connect_AP(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))
            time.sleep(1)
    while not mqtt_client.is_connected():
        print(f"Connecting to AIO...")
        mqtt_client.connect()
        time.sleep(1)


def reset():
    if wifi:
        pass
    else:
        esp.reset()
        # pass

# If there was a display before (protomatter, LCD, or E-paper), release it so
# we can create ours
displayio.release_displays()

# This next call creates the RGB Matrix object itself. It has the given width
# and height. bit_depth can range from 1 to 6; higher numbers allow more color
# shades to be displayed, but increase memory usage and slow down your Python
# code. If you just want to show primary colors plus black and white, use 1.
# Otherwise, try 3, 4 and 5 to see which effect you like best.
#


displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width=128, bit_depth=4,
    rgb_pins=[
        board.MTX_R1,
        board.MTX_G1,
        board.MTX_B1,
        board.MTX_R2,
        board.MTX_G2,
        board.MTX_B2
    ],
    addr_pins=[
        board.MTX_ADDRA,
        board.MTX_ADDRB,
        board.MTX_ADDRC,
        board.MTX_ADDRD
    ],
    clock_pin=board.MTX_CLK,
    latch_pin=board.MTX_LAT,
    output_enable_pin=board.MTX_OE
)

# Associate the RGB matrix with a Display so that we can use displayio features
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

# Set up wifi
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)

# Get Adafruit IO data
mqtt_topic = "prcutler/feeds/audio"
aio_username = os.getenv("AIO_USERNAME")
aio_key = os.getenv("AIO_KEY")

aio = IO_HTTP(aio_username, aio_key, requests)

try:
    data = aio.receive_data('audio')
    print(data, type(data))

    data_json = json.loads(data["value"])
    print(data_json)
    print("Song: ", data_json["title"] + " by " + data_json["artist"])

    song_title = data_json["title"]
    song_artist = data_json["artist"]

    song_title_scroll = song_title + '        '
    song_artist_scroll = song_artist + '         '



except:
    print("Adafruit IO reports 404 Error - is your feed empty?  Start recording.")

# Create two lines of text to scroll. Besides changing the text, you can also
# customize the color and font (using Adafruit_CircuitPython_Bitmap_Font).
# To keep this demo simple, we just used the built-in font.
# The Y coordinates of the two lines were chosen so that they looked good
# but if you change the font you might find that other values work better.

line1 = adafruit_display_text.label.Label(
    terminalio.FONT,
    color=0xff0000,
    text=song_title_scroll)
line1.x = display.width
line1.y = 8

line2 = adafruit_display_text.label.Label(
    terminalio.FONT,
    color=0x0080ff,
    text=song_artist_scroll)
line2.x = display.width
line2.y = 24

# Put each line of text into a Group, then show that group.
g = displayio.Group()
g.append(line1)
g.append(line2)
display.root_group = g

# This function will scoot one label a pixel to the left and send it back to
# the far right if it's gone all the way off screen. This goes in a function
# because we'll do exactly the same thing with line1 and line2 below.
def scroll(line):
    line.x = line.x - 1
    line_width = line.bounding_box[2]
    if line.x < -line_width:
        line.x = display.width

# This function scrolls lines backwards.  Try switching which function is
# called for line2 below!
def reverse_scroll(line):
    line.x = line.x + 1
    line_width = line.bounding_box[2]
    if line.x >= display.width:
        line.x = -line_width

# MQTT
def connected(client, userdata, flags, rc):
    print("Subscribing to %s" % mqtt_topic)
    client.subscribe(mqtt_topic)


def disconnected(client, userdata, rc):
    print("Disconnected from MQTT Broker!")


def publish(client, userdata, topic, pid):
    print('Published to {0} with PID {1}'.format(topic, pid))


def message(client, topic, payload):
    print("mqtt msg:", topic, payload)

    payload_data = json.loads(payload)
    print(payload_data, type(payload_data))

    print("Song: ", payload_data["title"] + " by " + payload_data["artist"])

    song_title = payload_data["title"]
    song_artist = payload_data["artist"]

    song_title_scroll = song_title + '        '
    song_artist_scroll = song_artist + '         '

    line1 = song_title_scroll
    line2 = song_artist_scroll
    time.sleep(3)

# You can add more effects in this loop. For instance, maybe you want to set the
# color of each label to a different value.
# while True:
#    scroll(line1)
#    scroll(line2)
#    reverse_scroll(line2)
#    display.refresh(minimum_frames_per_second=0)
#
if wifi:
    mqtt_client = MQTT.MQTT(
        broker="io.adafruit.com",
        port=1883,
        username=os.getenv('AIO_USERNAME'),
        password=os.getenv('AIO_KEY'),
        socket_pool=pool,
        ssl_context=ssl_context,
        is_ssl=False,
        socket_timeout=0.01  # apparently socket recvs even block asyncio
    )
else:
    mqtt_client = MQTT.MQTT(
        broker="io.adafruit.com",
        username=os.getenv('AIO_USERNAME'),
        password=os.getenv('AIO_KEY'),
        socket_timeout=0.01  # apparently socket recvs even block asyncio
    )
    MQTT.set_socket(socket, esp)

mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_message = message
mqtt_client.on_publish = publish

# ASYNC

async def update_network():
    while True:
        try:
            connect_wifi_mqtt()
            mqtt_client.loop(0.2)
        except (RuntimeError, ConnectionError, MMQTTException) as ex:
            print(f"Exception: {ex} Resetting wifi...")
            reset()
            time.sleep(1)
        await asyncio.sleep(1)


async def update_ui():
    while True:
        scroll(line1)
        scroll(line2)
        display.refresh(minimum_frames_per_second=0)
        await asyncio.sleep(0.1)


async def main():
    net_task = asyncio.create_task(update_network())
    ui_task = asyncio.create_task(update_ui())
    await asyncio.gather(net_task, ui_task)

asyncio.run(main())
