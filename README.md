USBDetector
===========

Detects when an USB is plugged in and will then mount, attempt to send an EGG to that drive then unmount.

Text Files
===========

<<<<<<< HEAD
Script pulls an entire line from the selected text file.<br>
moose.txt can only have (a-b, 1-9,) spaces aloud and no caps.
=======
Script pulls an entire line from the selected text file.

morse.txt can only have (a-b, 1-9,) spaces aloud and no caps.
>>>>>>> origin/master

eggload.txt = Eggs to be placed on USB

badluck.txt = If egg is not selected pulls a line from this file

usedegg.txt = Eggs that have been picked by script are pulled from eggload and placed here

morse.txt = String to be used during moorse code method

usbdebug.log = generated file with debug from script

Usage
===========

To Start:
`python detect.py`

If the lights stay on after stopping the script use:
`python lightsoff.py`

Green LED = Plug in new USB

Yellow LED = Mounting/Sending egg/Unmounting

Blink Green LED = Safe to remove USB

Red LED = Error/Wait

Uses GPIO: 8_02, 8_15, 8_17, 8_19
