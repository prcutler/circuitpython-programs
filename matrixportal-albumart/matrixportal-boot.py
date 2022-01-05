import board
import digitalio
import storage

button_up = digitalio.DigitalInOut(board.BUTTON_UP)
# Default is that button is an input.
# Set a pullup so that the button will be high (True) if not pressed. 
button_up.pull = digitalio.Pull.UP

# If readonly is True, then CircuitPython cannot write to CIRCUITPY, but the host computer can.
# So if the button is pressed during reset, readonly=not button_up-value, which means readonly=True, and code.py will not be able to write
# to CIRCUITPY, but the host computer will be able to.
# You could set readonly=not switch.value instead to make the default the other way around.
# If 
storage.remount("/", readonly=not button_up.value)