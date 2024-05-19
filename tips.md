# CircuitPython Tips & Tricks
A collection of tips, tricks and methods I find myself needing on a regular basis.  Inspired by [todbot's repository](https://github.com/todbot/circuitpython-tricks) of CircuitPython tricks.

Table of Contents
=================
* [Networking](#networking)
* [Manage Files](#manage-files)


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

### Create a TCP socket
```
pool = socketpool.SocketPool(wifi.radio)
sock = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
```
(This creates an IPV4 TCP socket)

## Manage Files

### Rename a file

    `os.rename("old_name.txt", "new_name.txt")`

## Other

## Enable Logging
```
import adafruit_logging as logging
...
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
...
mqtt_client.logger = logger
```