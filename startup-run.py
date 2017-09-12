from dotstar import Adafruit_DotStar
from random import ranint
import time

strip = Adafruit_DotStar(NUMPIXELS, 2000000, order=order)

sizeX = 30
sizeY = 15

pixelGrid = [[0 for x in range(sizeX+1)] for y in range(sizeY+1)]

keyVal = 840
for j in range(sizeY):

    for i in range(sizeX):
	if(j % 2 == 0):
        	rawVal = keyVal + (i*2)
	else:
		rawVal = keyVal - (i*2)
        pixelGrid[j][i] = rawVal
        #print(pixelGrid[(sizeY-1)-j][i])

    if(j % 2 == 0):
        keyVal = keyVal - 2
    else:
        keyVal = keyVal - 118

strip.begin()

colours = [0xff0000, 0x00ff00, 0x0000ff]

for i in range
