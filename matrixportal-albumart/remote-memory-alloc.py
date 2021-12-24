# SPDX-FileCopyrightText: 2021 Tim C for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
imageload example for esp32s2 that loads an image fetched via
adafruit_requests using BytesIO
"""

img_bytes = bytearray(16384)

import io
import busio
#from digitalio import DigitalInOut
import adafruit_requests as requests
#import adafruit_esp32spi.adafruit_esp32spi_socket as socket
#from adafruit_esp32spi import adafruit_esp32spi
from adafruit_matrixportal.network import Network as network

import board
import displayio
import rgbmatrix
import framebufferio
import adafruit_imageload
import gc

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Setup Network
network = network(status_neopixel=board.NEOPIXEL, debug=False)
network.connect()

# Setup Display

displayio.release_displays()

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

url = "https://silversaucer.com/static/img/albumart/bg256.bmp"

print("Fetching image from %s" % url, "Free Memory: ", gc.mem_free())
response = requests.get(url)
print("GET complete")

bytes_img = io.BytesIO(response.content)

album_art = open("album_art.bmp", "wb")

album_art.write(bytes_img)
album_art.close()

#print("Type: ", type(bytes_img))img_bytes = io.BytesIO.read(bytes_img)
img_bytes = io.BytesIO.read(bytes_img)
image, palette = adafruit_imageload.load(img_bytes)
tile_grid = displayio.TileGrid(image, pixel_shader=palette)

group = displayio.Group(scale=1)
group.append(tile_grid)
display.show(group)

response.close()

while True:
    pass
