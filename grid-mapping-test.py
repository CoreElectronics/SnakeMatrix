from dotstar import Adafruit_DotStar

NUMPIXELS = 900

strip = Adafruit_DotStar(NUMPIXELS, 1000000)

strip.begin()
strip.show()

sizeX = 30
sizeY = 15

pixelGrid = [[0 for x in range(sizeX)] for y in range(sizeY)]

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

xpos = 2
ypos = 2

print(pixelGrid[ypos][xpos])
strip.setPixelColor(pixelGrid[ypos][xpos], 0xffffff)
strip.show()
