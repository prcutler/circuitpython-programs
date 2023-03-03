import board
# from adafruit_seesaw import seesaw, rotaryio, digitalio
import wifi
import socketpool
import os
import digitalio
import neopixel
import keypad

# Set up Receiver
HOST = "192.168.1.119"
PORT = 23

buffer = bytearray(1024)

# Setup wifi
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

# Connect to Receiver
try:
    pool = socketpool.SocketPool(wifi.radio)
    s = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
    s.connect((HOST, PORT))
except OSError:
    pool = socketpool.SocketPool(wifi.radio)
    s = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
    s.connect((HOST, PORT))
print("Connected!")


# Setup buttons
button0 = digitalio.DigitalInOut(board.D0)
button0.direction = digitalio.Direction.INPUT
button0.pull = digitalio.Pull.UP

button1 = digitalio.DigitalInOut(board.D1)
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.DOWN

button2 = digitalio.DigitalInOut(board.D2)
button2.direction = digitalio.Direction.INPUT
button2.pull = digitalio.Pull.DOWN

button0_state = False
button1_state = False
button2_state = False

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness = 0.6)


while True:

    # All values are TRUE
    # print(button0.value, button1.value, button2.value)

    if button0.value:
        print("Button 0")
    else:
        s.send(b"Z2AUX1\n")
        print("Changing input to CD")

    if not button1.value:
        print("Button 1")
    else:
        s.send(b"Z2TUNER\n")
        print("Changing input to TUNER")

    if not button2.value:
        print("Button 2")
    else:
        s.send(b"Z2CD\n")
        print("Changing input to Vinyl")

