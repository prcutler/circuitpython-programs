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
import adafruit_framebuf


WIDTH = 64
HEIGHT = 32

displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width=64, bit_depth=6,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.D25, board.D24, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1,
    doublebuffer=True)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)
print("Display info: ", display.height, display.width)

buffer = bytearray(round(WIDTH * HEIGHT / 8))
fb = adafruit_framebuf.FrameBuffer(
    buffer, WIDTH, HEIGHT, buf_format=adafruit_framebuf.MVLSB
)

group = displayio.Group()
#t = displayio.Tilegrid()


#  array of colors for the LEDs
#  goes from purple to red
#  gradient generated using https://colordesigner.io/gradient-generator
heatmap = [0xb000ff,0xa600ff,0x9b00ff,0x8f00ff,0x8200ff,
           0x7400ff,0x6500ff,0x5200ff,0x3900ff,0x0003ff,
           0x0003ff,0x0047ff,0x0066ff,0x007eff,0x0093ff,
           0x00a6ff,0x00b7ff,0x00c8ff,0x00d7ff,0x00e5ff,
           0x00e0ff,0x00e6fd,0x00ecf6,0x00f2ea,0x00f6d7,
           0x00fac0,0x00fca3,0x00fe81,0x00ff59,0x00ff16,
           0x00ff16,0x45ff08,0x62ff00,0x78ff00,0x8bff00,
           0x9bff00,0xaaff00,0xb8ff00,0xc5ff00,0xd1ff00,
           0xedff00,0xf5eb00,0xfcd600,0xffc100,0xffab00,
           0xff9500,0xff7c00,0xff6100,0xff4100,0xff0000,
           0xff0000,0xff0000]

#  size of the FFT data sample
fft_size = 256

bitmap = displayio.Bitmap(display.width, display.height, len(heatmap))
print("Heatmap len: ", len(heatmap))

palette = displayio.Palette(len(heatmap))

tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

#  setup for onboard mic
mic = audiobusio.PDMIn(board.SCL, board.SDA,
                       sample_rate=16000, bit_depth=16)

#  use some extra sample to account for the mic startup
samples_bit = array.array('H', [0] * (fft_size+3))


#  sends visualized data to the RGB matrix with colors
def waves(data, y):
    offset = max(0, (13-len(data))//2)

    for x in range(min(13, len(data))):
        fb.pixel(x + offset, y, heatmap[int(data[x])])


# main loop
def main():
    #  value for audio samples
    max_all = 10
    #  variable to move data along the matrix
    scroll_offset = 0
    #  setting the y axis value to equal the scroll_offset
    y = scroll_offset

    while True:
        #  record the audio sample
        mic.record(samples_bit, len(samples_bit))
        #  send the sample to the ulab array
        samples = np.array(samples_bit[3:])
        #  creates a spectogram of the data
        spectrogram1 = spectrogram(samples)
        # spectrum() is always nonnegative, but add a tiny value
        # to change any zeros to nonzero numbers
        spectrogram1 = np.log(spectrogram1 + 1e-7)
        spectrogram1 = spectrogram1[1:(fft_size//2)-1]
        #  sets range of the spectrogram
        min_curr = np.min(spectrogram1)
        max_curr = np.max(spectrogram1)
        #  resets values
        if max_curr > max_all:
            max_all = max_curr
        else:
            max_curr = max_curr-1
        min_curr = max(min_curr, 3)
        # stores spectrogram in data
        data = (spectrogram1 - min_curr) * (51. / (max_all - min_curr))
        # sets negative numbers to zero
        data = data * np.array((data > 0))
        #  resets y
        y = scroll_offset
        #  runs waves to write data to the LED's
        waves(data, y)
        #  updates scroll_offset to move data along matrix
        scroll_offset = (y + 1) % 9
        #  writes data to the RGB matrix
        display.refresh()


main()
