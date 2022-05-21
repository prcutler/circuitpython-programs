# SPDX-FileCopyrightText: 2019 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import board
from adafruit_pyportal import PyPortal



# Set up where we'll be fetching data from
DATA_SOURCE = "https://silversaucer.com/album/data"

# There's a few different places we look for data in the photo of the day
image_location = ["image_url"]
artist = ["artist"]
album = ["album"]

# the current working directory (where this file is)
cwd = ("/"+__file__).rsplit('/', 1)[0]
pyportal = PyPortal(url=DATA_SOURCE,
                    json_path=(artist, album),
                    status_neopixel=board.NEOPIXEL,
                    default_bg=cwd+"/nasa_background.bmp",
                    text_font=cwd+"/fonts/Arial-12.bdf",
                    text_position=((85, 260), (85, 280)),
                    text_color=(0xFFFFFF, 0xFFFFFF),
                    text_maxlen=(50, 50), # cut off characters
                    image_json_path=image_location,
                    image_resize=(320, 320),
                    image_position=(80, 0))

while True:
    response = None
    try:
        response = pyportal.fetch()
        print("Response is", response)
    except RuntimeError as e:
        print("Some error occurred, retrying! -", e)

    time.sleep(30*60)  # 30 minutes till next check
