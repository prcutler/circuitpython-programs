# SPDX-FileCopyrightText: 2019 Carter Nelson for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import board
import displayio
from adafruit_display_text import bitmap_label,  wrap_text_to_lines
import terminalio


display = board.DISPLAY

# Create a bitmap with two colors
bitmap = displayio.Bitmap(display.width, display.height, 2)

# Create a two color palette
palette = displayio.Palette(2)
palette[0] = 0x000000
palette[1] = 0xffffff

# Create a TileGrid using the Bitmap and Palette
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

# Create a Group
group = displayio.Group()

# Add the TileGrid to the Group
group.append(tile_grid)

# Add the Group to the Display
display.show(group)

# Draw even more pixels
for x in range(0, 240):
    for y in range(0, 135):
        bitmap[x, y] = 1

mute = bitmap_label.Label(terminalio.FONT, text="MUTED", scale=4, x=75, y=55,color=0xff0000)
group.append(mute)

# Loop forever so you can enjoy your image
while True:
    pass
