from board import *
import digitalio, analogio, time, usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# Sets select0-3 to positive n less than 16 in binary
def SetKeySelection(n: int, select: list):
    if n > 16 or n < 0:
        print("Key selection too great")
        return
    x = bin(n)[2:]
    for i in range(4 - len(x)):
        x = '0' + x
    for i in range(len(x)):
        select[i].value = True if x[i] == '1' else False

# Distance from the sensor at which to trigger the keystroke. No current discernable units, so you'll have to determine the right number yourself.
magnetDistance = 12;

led = digitalio.DigitalInOut(LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

am0Pin = analogio.AnalogIn(A1)
#Array of values for each am0 pin and whether or not they are pressed. True for pressed, False for released.
am0 = [[30, False] for i in range(16)]
# Keycodes for each corresponding pin on the multiplexer. If you want am0:4 to send caps lock instead of numpad 4, change am0Codes[4] to Keycode.CAPS_LOCK
am0Codes = [Keycode.KEYPAD_ZERO, Keycode.KEYPAD_FORWARD_SLASH, None, None, Keycode.KEYPAD_FOUR, None, Keycode.KEYPAD_SEVEN, Keycode.KEYPAD_FIVE, Keycode.KEYPAD_ONE, Keycode.KEYPAD_EIGHT, None, None, None, None, Keycode.KEYPAD_NUMLOCK, Keycode.KEYPAD_TWO]

am1Pin = analogio.AnalogIn(A0)
#Array of values for each am1 pin and whether or not they are pressed. True for pressed, False for released.
am1 = [[30, False] for i in range(16)]
# Keycodes for each corresponding pin on the multiplexer. If you want am1:4 to send caps lock instead of numpad 3, change am1Codes[4] to Keycode.CAPS_LOCK
am1Codes = [Keycode.KEYPAD_PERIOD, Keycode.KEYPAD_MINUS, None, None, Keycode.KEYPAD_THREE, None, Keycode.KEYPAD_NINE, Keycode.KEYPAD_PLUS, Keycode.KEYPAD_SIX, None, None, None, None, None, Keycode.KEYPAD_ASTERISK, Keycode.KEYPAD_ENTER]

select = [digitalio.DigitalInOut(C14), digitalio.DigitalInOut(B8), digitalio.DigitalInOut(B12), digitalio.DigitalInOut(A15)]
select[0].direction = digitalio.Direction.OUTPUT
select[1].direction = digitalio.Direction.OUTPUT
select[2].direction = digitalio.Direction.OUTPUT
select[3].direction = digitalio.Direction.OUTPUT

# Incorrect keys:
# 1 - should be am0:1, is am0:8
# 3 - should be am1:1, is am1:4
# 4 - should be am0:2, is am0:4
# 5 - should be am0:14, is am0:7
# 6 - should be am1:2, is am1:8
# numlock - should be am0:7, is am0:14
# / - Should be am0:8, is am0:1
# * - should be am1:7, is am1:14
# - - should be am1:8, is am1:1
# + - should be am1:14, is am1:7

# I have no idea why they are the way they are. Doesn't break much of anything, though. ¯\_(ツ)_/¯

keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

while True:
    for i in range(16):
        # Update value arrays
        SetKeySelection(i, select)
        am0[i][0] = am0Pin.value / 1000
        am1[i][0] = am1Pin.value / 1000

        # If there is a key attached to am0:i, am0:i has a magnet close enough to it, and am0:i isn't already pressed, press it. Also keep the LED on while a key is pressed.
        if am0Codes[i] != None and (am0[i][0] > (32 + magnetDistance) or am0[i][0] < (32 - magnetDistance)) and am0[i][1] == False:
            keyboard.press(am0Codes[i])
            am0[i][1] = True
            if led.value: led.value = False
        # Otherwise, release the key attached to am0:i if it isn't already released. Also keep the LED off while no keys are pressed.
        elif am0[i][1] == True:
            keyboard.release(am0Codes[i])
            am0[i][1] = False
            if not led.value: led.value = True

        # If there is a key attached to am1:i, am1:i has a magnet close enough to it, and am1:i isn't already pressed, press it. Also keep the LED on while a key is pressed.
        if am1Codes[i] != None and (am1[i][0] > (32 + magnetDistance) or am1[i][0] < (32 - magnetDistance)) and am1[i][1] == False:
            keyboard.press(am1Codes[i])
            am1[i][1] = True
            if led.value: led.value = False
        # Otherwise, release the key attached to am1:i if it isn't already released. Also keep the LED off while no keys are pressed.
        elif am1[i][1] == True:
            keyboard.release(am1Codes[i])
            am1[i][1] = False
            if not led.value: led.value = True