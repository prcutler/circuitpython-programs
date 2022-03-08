import digitalio
import board
import displayio

display = board.DISPLAY
display.rotation = 90

group = displayio.Group(scale=5, x=0, y=0)
group.x = 0
group.y = 160

image_file = open("/img/copperblue.bmp", "rb")
image = displayio.OnDiskBitmap(image_file)
image_sprite = displayio.TileGrid(image, pixel_shader=getattr(image, 'pixel_shader', displayio.ColorConverter()))

group.append(image_sprite)
board.DISPLAY.show(group)

while True:
    pass