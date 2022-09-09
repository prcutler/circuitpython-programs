# Courtesy of danh - to be used with a CPX

import time
import board
import digitalio
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

b = digitalio.DigitalInOut(board.BUTTON_B)
b.pull = digitalio.Pull.DOWN

start = time.time()
while True:
    if b.value:
        t = time.time() - start
        minutes = t // 60
        seconds = t % 60
        layout.write(f"{minutes:d}:{seconds:02d} ")
        time.sleep(0.3)


