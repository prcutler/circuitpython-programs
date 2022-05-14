from PIL import Image


size = (320, 320)
num_colors = 64
img = Image.open('cps-logo-500.jpg')
img = img.resize(size)
newimg = img.convert(mode='P', colors=num_colors)
newimg.save('cps-logo.bmp')