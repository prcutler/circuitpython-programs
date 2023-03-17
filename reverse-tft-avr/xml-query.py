# SPDX-FileCopyrightText: Copyright (c) 2022 Neradoc
# SPDX-License-Identifier: Unlicense

import sys
from ElementTree import parse
import adafruit_requests
import ssl
import wifi
import socketpool
import os
import ElementTree as ET


# Setup wifi
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

# Set up Receiver
HOST = "192.168.1.119"
PORT = 23

# Connect to the receiver
try:
    pool = socketpool.SocketPool(wifi.radio)
    s = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
    s.connect((HOST, PORT))
except OSError:
    pool = socketpool.SocketPool(wifi.radio)
    s = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
    s.connect((HOST, PORT))
print("Connected!")

requests = adafruit_requests.Session(pool, ssl.create_default_context())

url = "http://192.168.1.119:8080/goform/AppCommand.xml"

xml_body = '''
    <?xml version="1.0" encoding="utf-8"?>
    <tx>
        <cmd id="1">GetAllZoneVolume</cmd>
    </tx>'''

r = requests.post(url, data=xml_body)
print(r.text)

root = ET.fromstring(r.text)
print("Root Type: ", type(root), root)
print("Root tag: ", root.tag)

for cmd in root:
    print(cmd.tag, cmd.attrib)
    for zone in cmd:
        print(zone.tag, zone.attrib)
        for vol in zone:
            print("Tag: ", vol.tag, "Text: ", vol.text)

print(root[0][1][4].text)



#for zone2 in volumes:
#    print(zone2.text)

#with open("some-demo.xml", "r") as fp:
#    tree = parse(fp)
#    print("Tree type: ", type(tree), tree)

#def print_sub_tree(node, depth=0):
#    if node.text is not None:
#        text = '"' + node.text + '"'
#    else:
#        text = ""
#    print(" "*depth, "-", node.tag, text)
#    for key, value in node.attrib.items():
#        print(" "*depth, "|", key, ":", value)
#    for subnode in node:
#        print_sub_tree(subnode, depth+2)

#print_sub_tree(tree.getroot())