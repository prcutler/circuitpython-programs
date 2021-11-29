# MACROPAD Hotkeys : Onshape CAD for Mac

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values

app = {                    # REQUIRED dict, must be named 'app'
    'name' : 'Onshape', # Application name
    'macros'   : [           # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x004000, 'Iso', [Keycode.SHIFT, '7']), # Isometric (Home) View
        (0x004000, 'Front', [Keycode.SHIFT, '1']), # Front View
        (0x3a5fcd, 'Undo', [Keycode.SHIFT, 'Z']),  # Undo
        # 2nd row ----------
        (0x004000, 'Left', [Keycode.SHIFT, '3']),  # Left View
        (0x3a5fcd, 'Back', [Keycode.SHIFT, '2']),      # Back View
        (0x202000, 'Right', [Keycode.SHIFT, '4']),  # Right View
        # 3rd row ----------
        (0x000040, 'Zoom', 'F'),  # Zoom to fit
        (0x000040, 'Up', [Keycode.UP_ARROW]), # Up arrow
        (0xffd800, 'Planes', 'P'),  # Hide / Show Planes
        # 4th row ----------
        (0x000040, 'Left', [Keycode.LEFT_ARROW]),  # Left
        (0x000040, 'Down', [Keycode.DOWN_ARROW]),  # Down
        (0x000040, 'Right', [Keycode.RIGHT_ARROW]),  # Right
        # Encoder button ---
        # (0x000000, '', [Keycode.COMMAND, 'w']) # Close window/tab
]
}
