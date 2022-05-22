import time
from math import sin
import board
import displayio
import rgbmatrix
import framebufferio
import adafruit_imageload
import terminalio
from adafruit_display_text.label import Label
from adafruit_matrixportal.network import Network
import adafruit_requests as requests

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

url = 'https://silversaucer.com/static/img/album-art/image_300.bmp'
print(url)

response = requests.get(url)

path = 'album_art.bmp'

with open(path, 'wb',) as f:
    for chunk in response.iter_content(chunk_size=32):
        f.write(chunk)
    print("Album art saved")
response.close()


matrix = rgbmatrix.RGBMatrix(
    width=64, height=64, bit_depth=4, tile=2, serpentine=True,
    rgb_pins=[board.MTX_R1,
              board.MTX_G1,
              board.MTX_B1,
              board.MTX_R2,
              board.MTX_G2,
              board.MTX_B2],
    addr_pins=[board.MTX_ADDRA,
               board.MTX_ADDRB,
               board.MTX_ADDRC,
               board.MTX_ADDRD],
    clock_pin=board.MTX_CLK, latch_pin=board.MTX_LAT,
    output_enable_pin=board.MTX_OE)


display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)
g = displayio.Group()
b, p = adafruit_imageload.load("album_art.bmp")
t = displayio.TileGrid(b, pixel_shader=p)
t.x = 0
g.append(t)

display.show(g)

while True:

    display.show(g)
    display.refresh()
