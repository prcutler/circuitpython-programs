# SPDX-FileCopyrightText: 2021 John Furcean
# SPDX-License-Identifier: MIT

"""Code based on I2C rotary encoder simple test example."""

import board
from adafruit_seesaw import seesaw, rotaryio, digitalio
from secrets import secrets
import wifi
import socketpool
from adafruit_neokey.neokey1x4 import NeoKey1x4

# Set up Receiver
HOST = "192.168.1.119"
PORT = 23

buffer = bytearray(1024)

# wifi.radio.connect(secrets["ssid"], secrets["password"])
try:
    pool = socketpool.SocketPool(wifi.radio)
    s = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
    s.connect((HOST, PORT))
except OSError:
    pool = socketpool.SocketPool(wifi.radio)
    s = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
    s.connect((HOST, PORT))
print("Connected!")

# use default I2C bus
i2c_bus = board.STEMMA_I2C()

# Create a NeoKey object
neokey = NeoKey1x4(i2c_bus, addr=0x30)

rot_enc = seesaw.Seesaw(board.STEMMA_I2C(), addr=0x36)

seesaw_product = (rot_enc.get_version() >> 16) & 0xFFFF
print("Found product {}".format(seesaw_product))
if seesaw_product != 4991:
    print("Wrong firmware loaded?  Expected 4991")

rot_enc.pin_mode(24, rot_enc.INPUT_PULLUP)
button = digitalio.DigitalIO(rot_enc, 24)
button_held = False

encoder = rotaryio.IncrementalEncoder(rot_enc)
last_position = 0

def mute_check():
    z2_mute_check = s.send(b"Z2MU?\n")
    bytes_rec = s.recv_into(buffer)
    mute_response = bytearray.decode(buffer)
    print("Msg received")
    print("Type: ", mute_response)


def mute_toggle():
    s.send(b"Z2MU?\n")
    s.recv_into(buffer)
    mute_response = bytearray.decode(buffer)
    print("Type: ", type(mute_response), mute_response)
    print("Length: ", len(mute_response), mute_response[:7])
    if mute_response[:7] is 'Z2MUOFF':

        s.send(b'Z2MUON\n')
        print("Mute on")
    else:
        print("Hello")
        s.send(b"Z2MUOFF\n")
        print(mute_response is "Z2MUOFF")
        print("Mute off")

while True:

    # negate the position to make clockwise rotation positive
    position = -encoder.position

    if position != last_position:

        if last_position < position:
            s.send(b"Z2UP\n")
        else:
            s.send(b"Z2DOWN\n")
        last_position = position
        print("Position: {}".format(position))

    if not button.value and not button_held:
        button_held = True
        print("Button pressed")

    if button.value and button_held:
        button_held = False
        print("Button released")

    if neokey[0]:
        print("Button A")
        s.send(b"Z2AUX1\n")
        neokey.pixels[0] = 0xFF0000
    else:
        neokey.pixels[0] = 0x0

    if neokey[1]:
        print("Button B")
        s.send(b"Z2TUNER\n")
        neokey.pixels[1] = 0xFFFF00
    else:
        neokey.pixels[1] = 0x0

    if neokey[2]:
        print("Button C")
        s.send(b"Z2CD\n")
        neokey.pixels[2] = 0x00FF00
    else:
        neokey.pixels[2] = 0x0

    if neokey[3]:
        print("Button D")
        mute_toggle()
        neokey.pixels[3] = 0x00FFFF
    else:
        neokey.pixels[3] = 0x0
