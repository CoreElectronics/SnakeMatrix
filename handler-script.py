#!usr/bin/python
#import evdev
from evdev import InputDevice, categorize, ecodes
import subprocess
import time
import os
from dotstar import Adafruit_DotStar
import signal

sizeX = 30
sizeY = 15

NUMPIXELS = 2*sizeX*sizeY
ORDER = 'gbr'
SPI_FREQ = 16000000

strip = Adafruit_DotStar(NUMPIXELS, SPI_FREQ, order=ORDER)
strip.begin()
strip.show()

#button code variables (change to suit your device)
select_button = 49

counter = 0
num_scripts = 2

gamepad = InputDevice('/dev/input/event1')
cmd1 = "sudo python /home/pi/SnakeMatrix/sa-matrix-mic.py"
cmd2 = "sudo python snake-matrix.py"

#loop and filter by event code and print the mapped label
for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY and event.value == 1 and event.code == select_button:
	if counter == 0:
		print("Launching Spectrum Analyzer")
		p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE, shell=True)
		counter += 1

	elif counter == 1:
		os.makedirs("toggleYes")
		print("Launching Snake")
		p2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE, shell=True)
		counter = 0

