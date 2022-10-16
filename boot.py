import usb_cdc
import usb_hid

usb_cdc.disable()
usb_hid.enable((usb_hid.Device.KEYBOARD,))