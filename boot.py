from board import *
import digitalio, analogio, usb_cdc, usb_hid, storage

magnetDistance = 12

storage.disable_usb_drive()
usb_cdc.disable()
usb_hid.enable((usb_hid.Device.KEYBOARD,))

select0 = digitalio.DigitalInOut(C14)
select0.direction = digitalio.Direction.OUTPUT
select1 = digitalio.DigitalInOut(B8)
select1.direction = digitalio.Direction.OUTPUT
select2 = digitalio.DigitalInOut(B12)
select2.direction = digitalio.Direction.OUTPUT
select3 = digitalio.DigitalInOut(A15)
select3.direction = digitalio.Direction.OUTPUT

select0.value = True
select1.value = True
select2.value = True
select3.value = False

am0Pin = analogio.AnalogIn(A1)

if am0Pin.value / 1000 > (32 + magnetDistance) or am0Pin.value < (32 - magnetDistance):
    storage.enable_usb_drive()