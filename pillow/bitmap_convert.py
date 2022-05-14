from PIL import Image


size = (500,500)
num_colors = 16
img = Image.open('cps-logo-500.jpg')
img = img.resize(size)
newimg = img.convert(mode='P', colors=num_colors)
newimg.save('16-cps-logo-500.bmp')