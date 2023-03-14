import requests
import xml.etree.ElementTree as ET



def get_volume():

    url = "http://192.168.1.119:8080/goform/AppCommand.xml"

    xml_body = '''
        <?xml version="1.0" encoding="utf-8"?>
        <tx>
            <cmd id="1">GetAllZoneVolume</cmd>
        </tx>'''

    r = requests.post(url, xml_body)
    # print(r.text)

    volume_response = str(r.text)
    print(volume_response)
    root = ET.fromstring(volume_response)

    for vol in root.findall("./rx/cmd/zone2/dispvalue"):
        print(vol.attrib)

    
get_volume()