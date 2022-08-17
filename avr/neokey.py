import wifi
import socketpool
import time
from secrets import secrets
import board
from adafruit_neokey.neokey1x4 import NeoKey1x4


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


# Check each button, if pressed, light up the matching neopixel!
while True:
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

