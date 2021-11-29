# MACROPAD Hotkeys : Onshape CAD for Mac

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values

app = {                    # REQUIRED dict, must be named 'app'
    'name' : 'Onshape', # Application name
    'macros'   : [           # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x228b22, 'Iso', [Keycode.SHIFT, '7']), # Isometric (Home) View - Forest Green
        (0x191970, 'Front', [Keycode.SHIFT, '1']), # Front View
        (0xff0800, 'Undo', [Keycode.SHIFT, 'Z']),  # Undo - Candy Apple Red
        # 2nd row ----------
        (0x191970, 'Left', [Keycode.SHIFT, '3']),  # Left View
        (0x191970, 'Back', [Keycode.SHIFT, '2']),      # Back View
        (0x191970, 'Right', [Keycode.SHIFT, '4']),  # Right View
        # 3rd row ----------
        (0x228b22, 'Zoom', 'F'),  # Zoom to fit
        (0x000080, 'Up', [Keycode.UP_ARROW]), # Up arrow
        (0xffef00, 'Planes', 'p'),  # Hide / Show Planes - Canary Yellow
        # 4th row ----------
        (0x000080, 'Left', [Keycode.LEFT_ARROW]),  # Left
        (0x000080, 'Down', [Keycode.DOWN_ARROW]),  # Down
        (0x000080, 'Right', [Keycode.RIGHT_ARROW]),  # Right
        # Encoder button ---
        # (0x000000, '', [Keycode.COMMAND, 'w']) # Close window/tab
]
}
