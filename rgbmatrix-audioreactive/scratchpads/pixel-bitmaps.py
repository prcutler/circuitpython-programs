# SPDX-FileCopyrightText: 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
from math import sin
import board
import displayio
import rgbmatrix
import framebufferio
import adafruit_imageload
import terminalio
import terminalio
from adafruit_display_text.label import Label

displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width=64, bit_depth=6,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.D25, board.D24, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1,
    doublebuffer=True)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

# Create a two color palette
palette = displayio.Palette(4)
palette[0] = 0x000000
palette[1] = 0x00FF00 # Blue
palette[2] = 0x0000FF # Green
palette[3] = 0xFF0000 # Red

# Create a bitmap with two colors
bitmap = displayio.Bitmap(display.width, display.height, len(palette))

# Create a TileGrid using the Bitmap and Palette
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

# Create a Group
group = displayio.Group()

# Add the TileGrid to the Group
group.append(tile_grid)

# Add the Group to the Display
display.show(group)

# Draw a pixel
bitmap[55, 5] = 1
bitmap[55, 6] = 2

# Draw even more pixels
for x in range(5, 30):
    for y in range(10, 30):
        bitmap[x, y] = 1


target_fps = 60

while True:
    display.refresh(target_frames_per_second=target_fps, minimum_frames_per_second=0)
