# SPDX-FileCopyrightText: 2021 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: MIT

'''Adapted from the FFT Example: Waterfall Spectrum Analyzer
by Jeff Epler
https://learn.adafruit.com/ulab-crunch-numbers-fast-with-circuitpython/overview and
https://learn.adafruit.com/mini-led-matrix-audio-visualizer'''

import array
import board
import audiobusio
import busio
from ulab import numpy as np
from ulab.scipy.signal import spectrogram
import rgbmatrix
import framebufferio
import displayio
import adafruit_imageload
from adafruit_display_text.label import Label
import terminalio
import time
from math import sin


displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width=64, bit_depth=6,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.D25, board.D24, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1,
    doublebuffer=True)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)
print("Display info: ", display.height, display.width)


g = displayio.Group()
b, p = adafruit_imageload.load("pi-logo32b.bmp")
t = displayio.TileGrid(b, pixel_shader=p)
t.x = 20
g.append(t)


display.show(g)

while True:
    display.refresh(target_frames_per_second=50, minimum_frames_per_second=0)
