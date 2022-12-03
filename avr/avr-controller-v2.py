"""Code based on I2C rotary encoder simple test example. by John Furcean under an MIT license"""

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

#  states for key presses
key_0_state = False
key_1_state = False
key_2_state = False
key_3_state = False


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
        neokey.pixels.fill(0xFF0000)

    else:
        print("Hello")
        s.send(b"Z2MUOFF\n")
        neokey.pixels.fill(0x0)
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


    #  Debounce Setup
    #  TODO: Figure out lights
    if not neokey[0] and key_0_state:
        key_0_state = False
        neokey.pixels[0] = 0x0
    if not neokey[1] and key_1_state:
        key_1_state = False
        neokey.pixels[1] = 0x0
    if not neokey[2] and key_2_state:
        key_2_state = False
        neokey.pixels[2] = 0x0
    if not neokey[3] and key_3_state:
        key_3_state = False
        neokey.pixels[3] = 0x0

    #  Button 1
    if neokey[0] and not key_0_state:
        print("Button A")
        #  turn on NeoPixel
        neokey.pixels[0] = 0xFF0000
        s.send(b"Z2AUX1\n")
        key_0_state = True

    #  Button 2
    if neokey[1] and not key_1_state:
        print("Button B")
        #  turn on NeoPixel
        neokey.pixels[1] = 0xFF0000
        s.send(b"Z2TUNER\n")
        key_1_state = True

    #  Button 3
    if neokey[2] and not key_2_state:
        print("Button C")
        #  turn on NeoPixel
        neokey.pixels[2] = 0xFF0000
        s.send(b"Z2CD\n")
        key_2_state = True

    #  Button 4
    if neokey[3] and not key_3_state:
        print("Button D")
        #  turn on NeoPixel
        # neokey.pixels[3] = 0xFF0000
        mute_toggle()
        key_3_state = True
