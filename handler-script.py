#!usr/bin/python
#import evdev
from evdev import InputDevice, categorize, ecodes
import subprocess
import time
import os

#button code variables (change to suit your device)
select_button = 49

counter = 0
num_scripts = 2
firstCycle = True

gamepad = InputDevice('/dev/input/event0')
cmd1 = "python /home/pi/SnakeMatrix/sa-matrix-mic.py"
cmd2 = "python snake-matrix.py"

#loop and filter by event code and print the mapped label
for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY and event.value == 1 and event.code == select_button:
	if counter == 0:
		if os.path.exists('/home/pi/SnakeMatrix/toggleYes'):
			os.rmdir('/homepi/SnakeMatrix/toggleYes')
		time.sleep(0.5)
		print("Launching Spectrum Analyzer")
		p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE, shell=True)
		counter += 1
		firstCycle = False
	elif counter == 1:
		os.makedirs('/home/pi/SnakeMatrix/toggleYes')
		print("Launching Snake")
		time.sleep(0.5)
		p2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE, shell=True)
		counter = 0

