
# MACROPAD Hotkeys: Reaper DAW

from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode


app = {
    'name' : 'Reaper',
    'order': 4,  # Application order on the keyboard
    'macros' : [
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x0000ff, 'CH_L    ', [Keycode.'[']),
        (0x0000ff, 'Home    ', [Keycode.HOME]),
        (0x0000ff, 'CH_R', [Keycode.']']),
        # 2nd row ----------
        (0x0000ff, 'Z_IN    ', [Keycode.PLUS),
        (0x0000ff, 'Down    ', [Keycode.DOWN_ARROW]),
        (0x0000ff, 'Z_OUT', [Keycode.MINUS]),
        # 3rd row ----------
        (0xeeeeee, 'Cut    ', [Keycode.Z]),
        (0x00ff00, 'BRTH    ', [Keycode.A]),
        (0xeeeeee, 'RIP ', [Keycode.X]),
        # 4th row ----------
        (0x00ff00, 'Left', [Keycode.LEFT_ALT, Keycode.LEFT_ARROW]),
        (0x00ff00, 'PG DWN', [Keycode.PAGE_DOWN]),
        (0x00ff00, 'Right', [Keycode.LEFT_ALT, Keycode.RIGHT_ARROW]),
    ]
}