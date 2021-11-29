# MACROPAD Hotkeys : Onshape CAD for Mac

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values

app = {                    # REQUIRED dict, must be named 'app'
    'name' : 'onshape', # Application name
    'macros' : [           # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x004000, 'Iso', [Keycode.SHIFT, '7']), # Isometric (Home) View
        (0x004000, 'Front', [Keycode.SHIFT, '1']), # Front View
        (0x400000, 'Back', [Keycode.SHIFT, '2 ']),      # Back View
        # 2nd row ----------
        (0x202000, 'Undo', [Keycode.SHIFT, 'Z'), # Undo
        (0x202000, 'Up', [UP_ARROW]), # Up
        (0x400000, 'Planes', 'P'),   #  Hide / Show Planes
        # 3rd row ----------
        (0x000040, 'Left', [LEFT_ARROW]),  # Left
        (0x000040, 'Down', [DOWN_ARROW]), # Down
        (0x000040, 'Right', [RIGHT_ARROW,]), # Right
        # 4th row ----------
        (0x004000, 'Left', [Keycode.SHIFT, '3']), # Left View
        (0x004000, 'Bottom', [Keycode.SHIFT, '6']), # Bottom View
        (0x004000, 'Search', [Keycode.OPTION, 'C']), # Search Tools
        # Encoder button ---
        (0x000000, '', [Keycode.COMMAND, 'w']) # Close window/tab