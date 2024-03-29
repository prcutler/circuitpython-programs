# Overview
A collection of programs and tips I use with CircuitPython. Most of these files are just a scratchpad for the final project files.

## Projects & Code

### Audioreactive Featherwing
File: `code.py`

A rp2040 Feather with a Neopixel Feather and digital microphone.  The pixels move based on sound using a Fast Fourier Transformation (FFT). Learn more at its [project page](https://github.com/prcutler/speakerstand-lights/blob/main/pictures/neopixel-feather.gif) or [GitHub repository](https://github.com/prcutler/speakerstand-lights).

### MacroPad
File: `code.py` (no changes from the default Adafruit project)

`/macros`: My macros for my Adafruit MacroPad including Audacity, Safari, and more.

### MatrixPortal AlbumArt
Abandoned project to display album art on a 64x64 LED matrix.

### Pillow
Test scripts to manipulate images using Python.

### PyPortal Album Art
File: `pyportal-albumart.py` (Rename to `code.py` if using)

Using a PyPortal Titano, when I am logged into my website, silversaucer.com, I can have the site pick a random record.  That record's cover art is then displayed on the PyPortal.  Includes a number of scratchpad files, including a non-working version using MQTT and the `PyPortal` class.  (They work individually, but not together.)

# CircuitPython Tips & Tricks
A collection of tips, tricks and methods I find myself needing on a regular basis.  Inspired by [todbot's repository](https://github.com/todbot/circuitpython-tricks) of CircuitPython tricks.

Table of Contents
=================
* [Networking](#networking)
* [Manage Files](#manage-files)
* [Adafruit HID Keycodes](#adafruit-hid-keycodes)
* [Filesystem](#other)


## Networking
### Stream File Download
```
response = requests.get(url)
if response.status_code == 200:
    with open("albumart.bmp", "wb") as f:
        for chunk in response.iter_content(chunk_size=32):
            f.write(chunk)
        print("Album art saved")
    response.close()
```

### ESP32-S2 WiFi Connect 
```py
# Connect to WiFi
print("\n===============================")
print("Connecting to WiFi...")
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())
while not wifi.radio.ipv4_address:
    try:
        wifi.radio.connect(secrets['ssid'], secrets['password'])
    except (ConnectionError) as e:
        print("Connection Error:", e)
        print("Retrying in 10 seconds")
    time.sleep(10)
print("Connected!\n")
```

### Fetch a JSON file
```
import time
import wifi
import socketpool
import ssl
import adafruit_requests
from secrets import secrets
wifi.radio.connect(ssid=secrets['ssid'],password=secrets['password'])
print("my IP addr:", wifi.radio.ipv4_address)
pool = socketpool.SocketPool(wifi.radio)
session = adafruit_requests.Session(pool, ssl.create_default_context())
while True:
    response = session.get("https://silversaucer.com/album/data)"
    data = response.json()
    print("data:", data)
    time.sleep(5)
```

## Buttons

Neokey debouncing example:

```
prev_neokey0 = neokey[0]

while True:
    cur_neokey0 = neokey[0]
    if cur_neokey0 and not prev_neokey0:
        print("Button A Press")
    elif not cur_neokey0 and prev_neokey0:
        print("Button A Release")
    
    prev_neokey0 = cur_neokey0
```

## Manage Files

### Erase Filesystem

In `code.py`:
```
import storage
storage.erase_filesystem()
```

### Rename a file

    `os.rename("old_name.txt", "new_name.txt")`

### Read WAV file data (courtesy of todbot)
```
file = open("mywav.wav", "rb")
b = bytearray(1024)  # read 1024 bytes at a time
while file.readinto(b):
  print(b)
file.close()
```

## Adafruit HID Keycodes
* A handy list for MacroPad programming of [all the available keycodes](https://docs.circuitpython.org/projects/hid/en/latest/api.html#adafruit-hid-keycode-keycode).
* [Extended list of HID keycodes](https://github.com/Neradoc/CircuitPython_consumer_control_extended/blob/main/consumer_control_extended.py) by Neradoc

## Other

### Customize USB Device
* How to [disable the USB drive](https://learn.adafruit.com/customizing-usb-devices-in-circuitpython/circuitpy-midi-serial)