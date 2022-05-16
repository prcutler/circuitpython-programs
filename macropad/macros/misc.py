
# MACROPAD Hotkeys: Universal Numpad

from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode


app = {
    'name' : 'Misc',
    #'order': 5, # Application order on the keyboard
    'macros' : [
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x0000ff, 'PLAY   ', [[ConsumerControlCode.PLAY_PAUSE]]),
        (0x0000ff, 'Vol Up    ', [[ConsumerControlCode.VOLUME_INCREMENT]]),
        (0xff0000, 'Mute    ', [[ConsumerControlCode.MUTE]]),
        # 2nd row ----------
        (0x0000ff, 'PREV    ', [[ConsumerControlCode.SCAN_PREVIOUS_TRACK]]),
        (0x0000ff, 'VolDwn    ', [[ConsumerControlCode.VOLUME_DECREMENT]]),
        (0x0000ff, 'NEXT', [[ConsumerControlCode.SCAN_NEXT_TRACK]]),
        # 3rd row ----------
        (0xeeeeee, 'F5    ', [Keycode.F5]),
        (0x00ff00, 'Pg Up    ', [Keycode.PAGE_UP]),
        (0xeeeeee, 'PrScr ', [Keycode.SHIFT, Keycode.COMMAND, Keycode.FOUR]), #SHIFT CMD 4
        # 4th row ----------
        (0x00ff00, 'HOME', [Keycode.HOME]),
        (0x00ff00, 'PG DWN   ', [Keycode.PAGE_DOWN]),
        (0x00ff00, 'END  ', [Keycode.END]),
    ]
}