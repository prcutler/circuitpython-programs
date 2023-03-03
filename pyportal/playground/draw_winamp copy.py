# SPDX-FileCopyrightText: 2019 Carter Nelson for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import board
import displayio
import adafruit_imageload

display = board.DISPLAY

winamp, palette = adafruit_imageload.load("/image_320.bmp",
                                          winamp=displayio.Bitmap,
                                          palette=displayio.Palette)


# Create a TileGrid to hold the bitmap
tile_grid_1 = displayio.TileGrid(winamp, pixel_shader=palette)

# Create a Group to hold the TileGrid
group = displayio.Group()

# Add the TileGrid to the Group
group.append(tile_grid)




# Add the Group to the Display
display.show(group)

# Loop forever so you can enjoy your image
while True:
    pass
