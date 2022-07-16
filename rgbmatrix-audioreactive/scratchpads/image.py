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

g = displayio.Group()
b, p = adafruit_imageload.load("pi-logo32b.bmp")
t = displayio.TileGrid(b, pixel_shader=p)
t.x = 20
g.append(t)

bitmap = displayio.Bitmap(5, 5, 1)
display.show(bitmap)

l = Label(text="Feather\nRP2040", font=terminalio.FONT, color=0xffffff, line_spacing=.7)
l.x = 10
l.y = 10
g.append(l)

display.show(g)

target_fps = 60

while True:
    display.refresh(target_frames_per_second=target_fps, minimum_frames_per_second=0)
