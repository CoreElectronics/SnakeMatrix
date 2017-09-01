sizeX = 30
sizeY = 15

pixelGrid = [[0 for y in range(sizeX)] for x in range(sizeY)]

keyVal = 840
for j in range(sizeX):
    
    for i in range(sizeY):
        rawVal = keyVal + (i*2)
        pixelGrid[i][j] = rawVal
        #print(pixelGrid[(sizeY-1)-j][i])
        
    if(j % 2 == 0):
        keyVal = keyVal - 2
    else:
        keyVal = keyVal - 118
print(pixelGrid[1][14])
