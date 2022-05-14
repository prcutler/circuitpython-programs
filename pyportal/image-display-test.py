import time, board, displayio


display = board.DISPLAY
maingroup = displayio.Group(y=80) # everything goes in maingroup
display.show(maingroup) # show main group
bitmap = displayio.OnDiskBitmap(open("albumart.bmp", "rb"))
image = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
maingroup.append(image) #