#import evdev
from evdev import InputDevice, categorize, ecodes
import subprocess
import time
import os
import signal
from dotstar import Adafruit_DotStar

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

gamepad = InputDevice('/dev/input/event3')
cmd1 = "python sa-matrix-mic.py"
cmd2 = "python snake-matrix.py"
firstCycle = True

#loop and filter by event code and print the mapped label
for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY and event.value == 1 and event.code == select_button:
	if counter == 0:
		if firstCycle == False:
			p2.kill()
			strip.clear()
			strip.show()
		print("Launching Spectrum Analyzer")
		p1 = subprocess.Popen("exec " + cmd1, stdout=subprocess.PIPE, shell=True)
		counter += 1

	elif counter == 1:
		p1.kill()
		strip.clear()
		strip.show()
		print("Launching Snake")
		p2 = subprocess.Popen("exec " + cmd2, stdout=subprocess.PIPE, shell=True)
		firstCycle = False
		counter = 0

