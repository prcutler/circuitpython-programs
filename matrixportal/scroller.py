# SPDX-FileCopyrightText: 2023 Trevor Beaton for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import os
import time
import ssl
import wifi
import board
import terminalio
import socketpool
from adafruit_matrixportal.matrixportal import MatrixPortal
import adafruit_requests

SCROLL_DELAY = 0.03
time_interval = 5

text_color = 0xFC6900  # e.g., Retro Orange

# --- Wi-Fi setup ---
wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))
print(f"Connected to {os.getenv('CIRCUITPY_WIFI_SSID')}")

# --- Display setup ---
matrixportal = MatrixPortal(width=128, height=32, bit_depth=5, status_neopixel=board.NEOPIXEL, debug=True)

matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(0, (matrixportal.graphics.display.height // 2) - 1),
    scrolling=True,
)

header_text_area = matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(0, (matrixportal.graphics.display.height // 6) - 1),
)

matrixportal.set_text("Upper left hand corner", header_text_area)


# --- Main Loop ---
while True:
    matrixportal.set_text("This is a test")
    matrixportal.set_text_color(text_color)
    matrixportal.scroll_text(SCROLL_DELAY)

    time.sleep(time_interval)
