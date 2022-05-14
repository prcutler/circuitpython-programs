import adafruit_requests as requests
from adafruit_pyportal import PyPortal
import adafruit_pyportal
import adafruit_imageload
import displayio
import board
import os

import gc

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

display = board.DISPLAY
pyportal = PyPortal()

# Connect to WiFi
print("Connecting to WiFi...")
pyportal.network.connect()
print("Connected!")

url = "https://silversaucer.com/static/img/album-art/image_300.bmp"
free_memory = gc.mem_free()
print("Free memory: ", free_memory)

print("Fetching image from %s" % url)
response = requests.get(url)
gc.collect()
# print("GET complete, Type: ", type(response.content))

response = requests.get(url)
if response.status_code == 200:
    with open("albumart.bmp", "wb") as f:
        for chunk in response.iter_content(chunk_size=32):
            f.write(chunk)
        print("Album art saved")
    response.close()

    print(os.listdir())

    # open('bg256.bmp', 'wb').write(response.content)
else:
    print("Bad get request")

group = displayio.Group(scale=1, x=0, y=0)
group.x = 0
group.y = 160

image_file = open("/albumart.bmp", "rb")
image = displayio.OnDiskBitmap(image_file)
image_sprite = displayio.TileGrid(image, pixel_shader=getattr(image, 'pixel_shader', displayio.ColorConverter()))

group.append(image_sprite)
board.DISPLAY.show(group)

while True:
    pass

