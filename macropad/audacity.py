
# MACROPAD Hotkeys: Universal Numpad

from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode


app = {
    'name' : 'Audacity',
    #'order': 4, # Application order on the keyboard
    'macros' : [
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x0000ff, 'Record   ', 'R'),
        (0x0000ff, 'Up    ', [Keycode.UP_ARROW]),
        (0xff0000, 'NEW    ', [Keycode.SHIFT, Keycode.R]),
        # 2nd row ----------
        (0x0000ff, 'START    ', [Keycode.HOME]),
        (0x0000ff, 'Down    ', [Keycode.DOWN_ARROW]),
        (0x0000ff, 'END', [Keycode.END]),
        # 3rd row ----------
        (0xeeeeee, 'F5    ', [Keycode.F5]),
        (0x00ff00, 'Pg Up    ', [Keycode.PAGE_UP]),
        (0xeeeeee, 'Pause ', 'P'),
        # 4th row ----------
        (0x00ff00, 'HOME', [Keycode.HOME]),
        (0x00ff00, 'PG DWN   ', [Keycode.PAGE_DOWN]),
        (0x00ff00, 'END  ', [Keycode.END]),
    ]
}