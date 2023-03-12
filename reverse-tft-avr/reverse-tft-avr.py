import board
from adafruit_seesaw import seesaw, rotaryio
from adafruit_seesaw import digitalio as seesawio
import wifi
import socketpool
import os
import digitalio
import neopixel
import displayio
from adafruit_progressbar.horizontalprogressbar import (
    HorizontalProgressBar,
    HorizontalFillDirection,
)
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import bitmap_label,  wrap_text_to_lines
from adafruit_debouncer import Debouncer
import terminalio


# Set up Receiver
HOST = "192.168.1.119"
PORT = 23

buffer = bytearray(1024)

# Setup wifi
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

# Make the display context
avr = displayio.Group()
board.DISPLAY.show(avr)

# set progress bar width and height relative to board's display
width = 183
height = 30

x = 28
#y = board.DISPLAY.height // 3
y = 100

# Create a new progress_bar object at (x, y)
progress_bar = HorizontalProgressBar(
    (x, y),
    (width, height),
    fill_color=0x000000,
    outline_color=0xFFFFFF,
    bar_color=0x0000ff,
    direction=HorizontalFillDirection.LEFT_TO_RIGHT
)

# Append progress_bar to the avr group
avr.append(progress_bar)

input = "Tuner"
vol = 51

progress_bar.value = vol

text = bitmap_label.Label(terminalio.FONT, text="Input: " + input, scale=2, x=28, y=25)
avr.append(text)

text2 = bitmap_label.Label(terminalio.FONT, text="Volume: " + str(vol), scale=2, x=28, y=65)
avr.append(text2)

# Connect to the receiver
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
button_0 = Debouncer(button0)

button1 = digitalio.DigitalInOut(board.D1)
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.DOWN
button_1 = Debouncer(button1)

button2 = digitalio.DigitalInOut(board.D2)
button2.direction = digitalio.Direction.INPUT
button2.pull = digitalio.Pull.DOWN
button_2 = Debouncer(button2)

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

        avr = displayio.Group()
        board.DISPLAY.show(avr)

        mute = bitmap_label.Label(terminalio.FONT, text="MUTED", scale=4, x=75, y=55)
        avr.append(mute)

    else:
        print("Hello")
        s.send(b"Z2MUOFF\n")
        print(mute_response is "Z2MUOFF")
        print("Mute off")

        avr = displayio.Group()
        board.DISPLAY.show(avr)
        progress_bar = HorizontalProgressBar(
            (x, y),
            (width, height),
            fill_color=0x000000,
            outline_color=0xFFFFFF,
            bar_color=0x0000ff,
            direction=HorizontalFillDirection.LEFT_TO_RIGHT
        )

        # Append progress_bar to the avr group
        avr.append(progress_bar)

        input = "Tuner"
        vol = 51

        progress_bar.value = vol

        text = bitmap_label.Label(terminalio.FONT, text="Input: " + input, scale=2, x=28, y=25)
        avr.append(text)

        text2 = bitmap_label.Label(terminalio.FONT, text="Volume: " + str(vol), scale=2, x=28, y=65)
        avr.append(text2)

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

    button_0.update()
    if button_0.fell:
        s.send(b"Z2AUX1\n")
        input = "CD"
        text = bitmap_label.Label(terminalio.FONT, text="Input: " + input, scale=2, x=28, y=25)
        avr.append(text)
        print("Changing input to CD")

    button_1.update()
    if button_1.fell:
        s.send(b"Z2TUNER\n")
        print("Changing input to TUNER")

    button_2.update()
    if button_2.fell:
        s.send(b"Z2CD\n")
        print("Changing input to Vinyl")
 