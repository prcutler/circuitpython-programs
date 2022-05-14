import requests

url = "https://silversaucer.com/static/img/album-art/image_300.bmp"
response = requests.get(url, stream=True)
if response.status_code == 200:
    with open("albumart.bmp", "wb") as f:
        for chunk in response.iter_content(chunk_size=32):
            f.write(chunk)
        f.close()
        print("File written")
    response.close()