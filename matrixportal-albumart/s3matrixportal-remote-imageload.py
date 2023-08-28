import displayio
from adafruit_matrixportal.matrix import Matrix
import os
import ssl

import adafruit_imageload
import adafruit_requests
import displayio
import socketpool
import wifi
from adafruit_matrixportal.matrix import Matrix

wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

displayio.release_displays()
matrix = Matrix(width=64, height=64, bit_depth=6)
display = matrix.display

url = "https://silversaucer.com/static/img/album-art/image64.bmp"
free_memory = gc.mem_free()
print("Free memory: ", free_memory)

print("Fetching image from %s" % url)
response = requests.get(url)
# print("GET complete, Type: ", type(response.content))

if response.status_code == 200:
    print("Starting image download...")
    with open("albumart.bmp", "wb") as f:
        for chunk in response.iter_content(chunk_size=32):
            f.write(chunk)
        print("Album art saved")
    response.close()

    # open('bg256.bmp', 'wb').write(response.content)

    group = displayio.Group(scale=1)
    b, p = adafruit_imageload.load("albumart.bmp")
    tile_grid = displayio.TileGrid(b, pixel_shader=p)
    # tile_grid.x = 0

    group.append(tile_grid)

    response.close()

    while True:
        display.show(group)

