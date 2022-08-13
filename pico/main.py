import argparse
from time import sleep

import belay

parser = argparse.ArgumentParser()
parser.add_argument("--port", "-p", default="/dev/cu.usbmodem113301")
args = parser.parse_args()

# Setup the connection with the micropython board.
# This also executes a few common imports on-device.
device = belay.Device(args.port)



@device.task
def read_temperature():
    # ADC4 is attached to an internal temperature sensor
    sensor_temp = ADC(4)
    reading = sensor_temp.read_u16()
    reading *= 3.3 / 65535  # Convert reading to a voltage.
    temperature = 27 - (reading - 0.706) / 0.001721  # Convert voltage to Celsius
    return temperature


while True:
    temperature = read_temperature()
    print(f"Temperature: {temperature:.1f}C")
    sleep(0.5)