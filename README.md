USBDetector
===========

Detects when an USB is plugged in and will then mount, attempt to send an EGG to that drive then unmount.

Green LED = safe to remove/plug in a new USB stick

Yellow LED = mount/sending egg/unmounting

Red LED = Error/Wait

Uses GPIO: 8_02, 8_10, 8_14, 8_18