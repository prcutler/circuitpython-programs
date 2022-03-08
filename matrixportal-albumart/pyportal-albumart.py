import time
from math import sin
import board
import displayio
import framebufferio
import adafruit_imageload
import terminalio
from adafruit_display_text.label import Label
from adafruit_pyportal.network import Network
import adafruit_requests as requests
from adafruit_pyportal import PyPortal

# Initialize hardware
displayio.release_displays()
NETWORK = Network(status_neopixel=board.NEOPIXEL, debug=False)
NETWORK.connect()

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

url = 'https://silversaucer.com/static/img/albumart/albumart.bmp'
print(url)

response = requests.get(url)

path = 'album_art.bmp'

with open(path, 'wb',) as f:
    f.write(response.content)


group = displayio.Group(scale=5, x=0, y=0)

image_file = open("album_art.bmp", "rb")
image = displayio.OnDiskBitmap(image_file)
image_sprite = displayio.TileGrid(image, pixel_shader=getattr(image, 'pixel_shader', displayio.ColorConverter()))

group.append(image_sprite)
board.DISPLAY.show(group)

while True:

    pass
