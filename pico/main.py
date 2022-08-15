import argparse
import time

import belay

parser = argparse.ArgumentParser()
parser.add_argument("--port", "-p", default="/dev/cu.usbmodem113301")
args = parser.parse_args()

# Setup the connection with the micropython board.
# This also executes a few common imports on-device.
device = belay.Device(args.port)


@device.task
def set_led(state):
    Pin(25, Pin.OUT).value(state)


while True:
    set_led(True)
    time.sleep(0.5)
    set_led(False)
    time.sleep(0.5)