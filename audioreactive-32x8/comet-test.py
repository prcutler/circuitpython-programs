# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example shows usage of the PixelMap helper to easily treat a single strip as a horizontal or
vertical grid for animation purposes.

For NeoPixel FeatherWing. Update pixel_pin and pixel_num to match your wiring if using
a different form of NeoPixels. Note that if you are using a number of pixels other than 32, you
will need to alter the PixelMap values as well for this example to work.

This example does not work on SAMD21 (M0) boards.
"""
import board
import neopixel

from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation import helper
from adafruit_led_animation.color import PURPLE, JADE, AMBER

# Update to match the pin connected to your NeoPixels
pixel_pin = board.A0
# Update to match the number of NeoPixels you have connected
pixel_num = 256

pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.2, auto_write=False)

#  32x8 needs alternating = True? - Need to use vertical?
pixel_wing_vertical = helper.PixelMap.vertical_lines(
    pixels, 32, 8, helper.vertical_strip_gridmap(8, alternating=True)
)

pixel_wing_horizontal = helper.PixelMap.horizontal_lines(
    pixels, 8, 32, helper.horizontal_strip_gridmap(8, alternating=False)
)

# The entire screen blinks green
# blink = Blink(pixels, speed=0.5, color=JADE)

# Appears to be inside out going vertically (starts in middle out mirrored?)
# rainbow_chase = RainbowChase(pixel_wing_vertical, speed=0.1, size=5, spacing=3)
# chase = Chase(pixel_wing_vertical, speed=0.1, size=3, spacing=6, color=AMBER)

# The pixel snakes up and down then moves horizontally left to right and then right to left
# comet = Comet(pixels, speed=0.10, color=PURPLE, tail_length=1, bounce=True)

# With pixel_wing_vertical of 8: 1 strip of lights vertically moving horizontally l-r and then r-l
# comet = Comet(pixel_wing_vertical, speed=0.10, color=PURPLE, tail_length=1, bounce=True)

# 1 strip of lights vertical
# Identical to pixel_wing_vertical?! No - it disappears halfway through
comet = Comet(pixel_wing_horizontal, speed=0.10, color=PURPLE, tail_length=1, bounce=True)

animations = AnimationSequence(comet, advance_interval=3, auto_clear=True)

while True:
    animations.animate()
