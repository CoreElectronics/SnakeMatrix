from dotstar import Adafruit_DotStar
import time

sizeX = 30
sizeY = 15

NUMPIXELS = 2*sizeX*sizeY

ORDER = 'gbr'
strip = Adafruit_DotStar(NUMPIXELS, 16000000, order=ORDER)

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

#write character left to right then bottom to top
#character bounders = 4(x) * 5(y)
a = [[0,0],[0,1],[0,2],[0,3],[1,2],[1,4],[2,2],[2,4],[3,0],[3,1],[3,2],[3,3]]
alphabet = [a]

strip.begin()
strip.show()

for pixel in a:
	strip.setPixelColor(pixelGrid(a[pixel]), 0xffffff)
strip.show()
time.sleep(3)
strip.clear()
strip.show()
