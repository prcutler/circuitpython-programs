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
import time


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

# Add input and volume labels and data to display
input_label = bitmap_label.Label(terminalio.FONT, text="Input: ", scale=2, x=28, y=25)
avr.append(input_label)
input_text = bitmap_label.Label(terminalio.FONT, text=input, scale=2, x=110, y=25)
avr.append(input_text)

vol_label = bitmap_label.Label(terminalio.FONT, text="Volume: ", scale=2, x=28, y=65)
avr.append(vol_label)
vol_text = bitmap_label.Label(terminalio.FONT, text=str(vol), scale=2, x=120, y=65)
avr.append(vol_text)


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


z2_vol_check = s.send(b"Z2TUNER\n")
bytes_rec = s.recv_into(buffer)
vol_response = bytearray.decode(buffer)
print(vol_response)

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

        # Create a bitmap with two colors
        bitmap = displayio.Bitmap(display.width, display.height, 2)

        # Create a two color palette
        palette = displayio.Palette(2)
        palette[0] = 0x000000
        palette[1] = 0xffffff

        # Create a TileGrid using the Bitmap and Palette
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

        # Add the TileGrid to the Group
        avr.append(tile_grid)

        # Draw even more pixels
        for x in range(0, 240):
            for y in range(0, 135):
                bitmap[x, y] = 1

        mute = bitmap_label.Label(terminalio.FONT, text="MUTED", scale=4, x=75, y=55,color=0xff0000)
        avr.append(mute)

    else:
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

        # Add input and volume labels and data to display
        input_label = bitmap_label.Label(terminalio.FONT, text="Input: ", scale=2, x=28, y=25)
        avr.append(input_label)
        input_text = bitmap_label.Label(terminalio.FONT, text=input, scale=2, x=110, y=25)
        avr.append(input_text)

        vol_label = bitmap_label.Label(terminalio.FONT, text="Volume: ", scale=2, x=28, y=65)
        avr.append(vol_label)
        vol_text = bitmap_label.Label(terminalio.FONT, text=str(vol), scale=2, x=120, y=65)
        avr.append(vol_text)

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
        input_text = bitmap_label.Label(terminalio.FONT, text=input, scale=2, x=110, y=25)
        avr[2] = input_text
        print("Changing input to CD")

    button_1.update()
    if button_1.fell:
        s.send(b"Z2TUNER\n")
        input = "Tuner"

        input_text = bitmap_label.Label(terminalio.FONT, text=input, scale=2, x=110, y=25)
        avr[2] = input_text
        print("Changing input to TUNER")

    button_2.update()
    if button_2.fell:
        s.send(b"Z2CD\n")        
        input = "Vinyl"

        input_text = bitmap_label.Label(terminalio.FONT, text=input, scale=2, x=110, y=25)
        avr[2] = input_text
        print("Changing input to Vinyl")
 