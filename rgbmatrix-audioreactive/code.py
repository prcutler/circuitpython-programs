# SPDX-FileCopyrightText: 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import array
from math import sin
import board
import displayio
import rgbmatrix
import framebufferio
import audiobusio
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
    palette[51 - i] = pi

bitmap = displayio.Bitmap(display.width, display.height, len(palette))
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

group = displayio.Group(scale=3)
fft_size = 256

# Add the TileGrid to the Group
group.append(tile_grid)

# Add the Group to the Display
display.show(group)

# instantiate board mic
mic = audiobusio.PDMIn(board.SCL, board.SDA,
                       sample_rate=16000, bit_depth=16)

# use some extra sample to account for the mic startup
samples_bit = array.array('H', [0] * (fft_size + 3))


#  sends visualized data to the RGB matrix with colors
def waves(data, y):
    offset = max(0, (32 - len(data)) // 2)

    for x in range(min(32, len(data))):
        bitmap[x + offset, y] = int(data[x])


# Main Loop
def main():
    max_all = 10
    #  variable to move data along the matrix
    scroll_offset = 0
    #  setting the y axis value to equal the scroll_offset
    y = scroll_offset

    while True:
        mic.record(samples_bit, len(samples_bit))
        samples = np.array(samples_bit[3:])
        spectrogram1 = spectrogram(samples)
        # spectrum() is always nonnegative, but add a tiny value
        # to change any zeros to nonzero numbers
        spectrogram1 = np.log(spectrogram1 + 1e-7)
        spectrogram1 = spectrogram1[1:(fft_size // 2) - 1]
        min_curr = np.min(spectrogram1)
        max_curr = np.max(spectrogram1)

        if max_curr > max_all:
            max_all = max_curr
        else:
            max_curr = max_curr - 1

        print(min_curr, max_all)
        min_curr = max(min_curr, 3)
        # Plot FFT
        data = (spectrogram1 - min_curr) * (51. / (max_all - min_curr))
        # This clamps any negative numbers to zero
        data = data * np.array((data > 0))

        y = scroll_offset
        #  runs waves to write data to the LED's
        waves(data, y)
        #  updates scroll_offset to move data along matrix
        scroll_offset = (y + 1) % 9

        display.show(group)
        display.refresh(target_frames_per_second=60, minimum_frames_per_second=0)


main()