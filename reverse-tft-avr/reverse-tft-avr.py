import board
from adafruit_seesaw import seesaw, rotaryio
from adafruit_seesaw import digitalio as seesawio
import wifi
import socketpool
import os
import digitalio
import neopixel

# Set up Receiver
HOST = "192.168.1.119"
PORT = 23

buffer = bytearray(1024)

# Setup wifi
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

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

# Setup rotary encoder
rot_enc = seesaw.Seesaw(board.STEMMA_I2C(), addr=0x36)

seesaw_product = (rot_enc.get_version() >> 16) & 0xFFFF
print("Found product {}".format(seesaw_product))
if seesaw_product != 4991:
   print("Wrong firmware loaded?  Expected 4991")

rot_enc.pin_mode(24, rot_enc.INPUT_PULLUP)
button = seesawio.DigitalIO(rot_enc, 24)
button_held = False

encoder = rotaryio.IncrementalEncoder(rot_enc)
last_position = 0

# Setup buttons
button0 = digitalio.DigitalInOut(board.D0)
button0.direction = digitalio.Direction.INPUT
button0.pull = digitalio.Pull.UP

button1 = digitalio.DigitalInOut(board.D1)
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.DOWN

button2 = digitalio.DigitalInOut(board.D2)
button2.direction = digitalio.Direction.INPUT
button2.pull = digitalio.Pull.DOWN

button0_state = False
button1_state = False
button2_state = False

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness = 0.6)


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

     # Turn the volume up or down
    if position != last_position:

        if last_position < position:
            s.send(b"Z2UP\n")
        else:
            s.send(b"Z2DOWN\n")
        last_position = position
        print("Position: {}".format(position))

    # Toggle mute / unmute
    if not button.value and not button_held:
        button_held = True
        mute_toggle()
        print("Toggle mute")

    if button.value and button_held:
       button_held = False
       print("Button released")

    # All values are True False False
    # print(button0.value, button1.value, button2.value)

    if button0.value:
        print("Button 0")
    else:
        s.send(b"Z2AUX1\n")
        print("Changing input to CD")

    if not button1.value:
        print("Button 1")
    else:
        s.send(b"Z2TUNER\n")
        print("Changing input to TUNER")

    if not button2.value:
        print("Button 2")
    else:
        s.send(b"Z2CD\n")
        print("Changing input to Vinyl")
