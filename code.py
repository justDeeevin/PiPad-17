from board import *
import digitalio, analogio, time, usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

def SetKeySelection(n: int, select: list):
    if n > 16:
        print("Key selection too great")
        return
    x = bin(n)[2:]
    for i in range(4 - len(x)):
        x = '0' + x
    for i in range(len(x)):
        select[i].value = True if x[i] == '1' else False

led = digitalio.DigitalInOut(LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

am0Pin = analogio.AnalogIn(A1)
am0 = [[30, False] for i in range(16)]
am0Codes = [Keycode.KEYPAD_ZERO, Keycode.KEYPAD_FORWARD_SLASH, None, None, Keycode.KEYPAD_FOUR, None, Keycode.KEYPAD_SEVEN, Keycode.KEYPAD_FIVE, Keycode.KEYPAD_ONE, Keycode.KEYPAD_EIGHT, None, None, None, None, Keycode.KEYPAD_NUMLOCK, Keycode.KEYPAD_TWO]

am1Pin = analogio.AnalogIn(A0)
am1 = [[30, False] for i in range(16)]
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

keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

while True:
    for i in range(16):
        SetKeySelection(i, select)
        am0[i][0] = am0Pin.value / 1000
        am1[i][0] = am1Pin.value / 1000
        if am0Codes[i] != None and (am0[i][0] > 45 or am0[i][0] < 20) and am0[i][1] == False:
            keyboard.press(am0Codes[i])
            am0[i][1] = True
            if led.value: led.value = False
        elif am0[i][1] == True:
            keyboard.release(am0Codes[i])
            am0[i][1] = False
            if not led.value: led.value = True

        if am1Codes[i] != None and (am1[i][0] > 45 or am1[i][0] < 20) and am1[i][1] == False:
            keyboard.press(am1Codes[i])
            am1[i][1] = True
            if led.value: led.value = False
        elif am1[i][1] == True:
            keyboard.release(am1Codes[i])
            am1[i][1] = False
            if not led.value: led.value = True