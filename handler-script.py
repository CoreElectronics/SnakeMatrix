#!usr/bin/python
import subprocess, time, os, sys
from dotstar import Adafruit_DotStar
from evdev import InputDevice, categorize, ecodes

sizeX = 30
sizeY = 15
NUMPIXELS = 2*sizeX*sizeY
strip = Adafruit_DotStar(NUMPIXELS, 8000000)
strip.begin()
strip.show()

counter = 1
select_button = 49

devID = '/dev/input/event1'
cmd1 = "sudo python /home/pi/SnakeMatrix/sa-matrix-mic.py"
cmd2 = "sudo python /home/pi/SnakeMatrix/snake-matrix.py"

p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE, shell=True)

while not os.path.exists(devID):
	time.sleep(0.01)

#loop and filter by event code and print the mapped label
def process_events():
	global counter
	global cmd1
	global cmd2
	toggleDir = '/home/pi/SnakeMatrix/toggleYes'
	try:
		gamepad = InputDevice(devID)
		for event in gamepad.read_loop():
			if event.type == ecodes.EV_KEY and event.value == 1 and event.code == select_button:
				if counter == 0:
					if os.path.exists(toggleDir):
						os.rmdir(toggleDir)
					time.sleep(0.5)
					print("Launching Spectrum Analyzer")
					p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE, shell=True)
					counter += 1
					#return False
		
				elif counter == 1:
					if not os.path.exists(toggleDir):
						os.makedirs(toggleDir)
					print("Launching Snake")
					time.sleep(0.5)
					p2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE, shell=True)
					counter = 0
	except:			
		return False
while True:
	process_events()
