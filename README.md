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
* [Adafruit HID Keycode](#adafruit-hid-keycode)


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


## Manage Files

### Rename a file

    `os.rename("old_name.txt", "new_name.txt")`

## Adafruit HID Keycodes
* A handy list for MacroPad programming of [all the available keycodes](https://docs.circuitpython.org/projects/hid/en/latest/api.html#adafruit-hid-keycode-keycode).