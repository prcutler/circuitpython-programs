import requests

url = 'https://silversaucer.com/static/img/album-art/image_300.bmp'
print(url)

response = requests.get(url)

saved_image = "album_art.bmp"

with open(saved_image, 'wb',) as f:
    f.write(response.content)