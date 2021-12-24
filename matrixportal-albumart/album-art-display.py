import time
from math import sin
import board
import displayio
import rgbmatrix
import framebufferio
import adafruit_imageload
import terminalio
from adafruit_display_text.label import Label



displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
    width=64, height=64, bit_depth=4, tile=2, serpentine=True,
    rgb_pins=[board.MTX_R1,
              board.MTX_G1,
              board.MTX_B1,
              board.MTX_R2,
              board.MTX_G2,
              board.MTX_B2],
    addr_pins=[board.MTX_ADDRA,
               board.MTX_ADDRB,
               board.MTX_ADDRC,
               board.MTX_ADDRD],
    clock_pin=board.MTX_CLK, latch_pin=board.MTX_LAT,
    output_enable_pin=board.MTX_OE)


display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)
g = displayio.Group()
b, p = adafruit_imageload.load("img/beasties64.bmp")
t = displayio.TileGrid(b, pixel_shader=p)
t.x = 0
g.append(t)

display.show(g)

while True:

    display.show(g)
    display.refresh()
