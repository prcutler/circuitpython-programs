
# MACROPAD Hotkeys: Reaper DAW

from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode


app = {
    'name' : 'Reaper',
    'macros' : [
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x1034a6, 'CH_L    ', [Keycode.LEFT_BRACKET]),
        (0x0000ff, 'Home    ', [Keycode.HOME]),
        (0x1034a6, 'CH_R', [Keycode.RIGHT_BRACKET]),
        # 2nd row ----------
        (0x0000ff, 'Z_IN    ', [Keycode.EQUALS]),
        (0x0000ff, 'End    ', [Keycode.END]),
        (0x0000ff, 'Z_OUT', [Keycode.MINUS]),
        # 3rd row ----------
        (0xce2029, 'CUT    ', [Keycode.Z]),
        (0xfffaf0, 'BRTH    ', [Keycode.A]),
        (0xce2029, 'RIP ', [Keycode.X]),
        # 4th row ----------
        (0x1034a6, 'Left', [Keycode.LEFT_ALT, Keycode.LEFT_ARROW]),
        (0x00ff00, 'Home', [Keycode.HOME]),
        (0x1034a6, 'Right', [Keycode.LEFT_ALT, Keycode.RIGHT_ARROW]),
    ]
}
