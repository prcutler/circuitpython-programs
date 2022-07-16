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
from ulab import numpy as np
from ulab.scipy.signal import spectrogram


displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width=64, bit_depth=6,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.D25, board.D24, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1,
    doublebuffer=True)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

# Create a heatmap color palette
palette = displayio.Palette(52)
for i, pi in enumerate((0xff0000, 0xff0a00, 0xff1400, 0xff1e00,
                        0xff2800, 0xff3200, 0xff3c00, 0xff4600,
                        0xff5000, 0xff5a00, 0xff6400, 0xff6e00,
                        0xff7800, 0xff8200, 0xff8c00, 0xff9600,
                        0xffa000, 0xffaa00, 0xffb400, 0xffbe00,
                        0xffc800, 0xffd200, 0xffdc00, 0xffe600,
                        0xfff000, 0xfffa00, 0xfdff00, 0xd7ff00,
                        0xb0ff00, 0x8aff00, 0x65ff00, 0x3eff00,
                        0x17ff00, 0x00ff10, 0x00ff36, 0x00ff5c,
                        0x00ff83, 0x00ffa8, 0x00ffd0, 0x00fff4,
                        0x00a4ff, 0x0094ff, 0x0084ff, 0x0074ff,
                        0x0064ff, 0x0054ff, 0x0044ff, 0x0032ff,
                        0x0022ff, 0x0012ff, 0x0002ff, 0x0000ff)):
    palette[51-i] = pi

class RollingGraph(displayio.TileGrid):
    def __init__(self, scale=2):
        # Create a bitmap with heatmap colors
        self.bitmap = displayio.Bitmap(display.width//scale,
                                       display.height//scale, len(palette))
        super().__init__(self.bitmap, pixel_shader=palette)

        self.scroll_offset = 0

    def show(self, data):
        y = self.scroll_offset
        bitmap = self.bitmap

        display.auto_refresh = False
        offset = max(0, (bitmap.width-len(data))//2)
        for x in range(min(bitmap.width, len(data))):
            bitmap[x+offset, y] = int(data[x])

        display.auto_refresh = True

        self.scroll_offset = (y + 1) % self.bitmap.height

group = displayio.Group(scale=3)
graph = RollingGraph(3)
fft_size = 256

# Add the TileGrid to the Group
group.append(graph)

# Add the Group to the Display
display.show(group)

# instantiate board mic
mic = audiobusio.PDMIn(board.SCL, board.SDA,
                       sample_rate=16000, bit_depth=16)

#use some extra sample to account for the mic startup
samples_bit = array.array('H', [0] * (fft_size+3))

# Main Loop
def main():
    max_all = 10

    while True:
        mic.record(samples_bit, len(samples_bit))
        samples = np.array(samples_bit[3:])
        spectrogram1 = spectrogram(samples)
        # spectrum() is always nonnegative, but add a tiny value
        # to change any zeros to nonzero numbers
        spectrogram1 = np.log(spectrogram1 + 1e-7)
        spectrogram1 = spectrogram1[1:(fft_size//2)-1]
        min_curr = np.min(spectrogram1)
        max_curr = np.max(spectrogram1)

        if max_curr > max_all:
            max_all = max_curr
        else:
            max_curr = max_curr-1

        print(min_curr, max_all)
        min_curr = max(min_curr, 3)
        # Plot FFT
        data = (spectrogram1 - min_curr) * (51. / (max_all - min_curr))
        # This clamps any negative numbers to zero
        data = data * np.array((data > 0))
        graph.show(data)

main()