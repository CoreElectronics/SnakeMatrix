import sys
import pyaudio
from struct import unpack
import numpy as np
from dotstar import Adafruit_DotStar

NUMPIXELS = 900

strip = Adafruit_DotStar(NUMPIXELS, 1600000)

strip.begin()
strip.show()

#setup grid mapping for matrix display
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

    if(j % 2 == 0):
        keyVal = keyVal - 2
    else:
        keyVal = keyVal - 118

#frequency response scaling
senseVal = 10
bassAdj = 1*senseVal
midAdj = 1*senseVal
trebleAdj = 3*senseVal

matrix    = [0 for x in range(30)]
power     = []
weighting = [1,1,1,1,2,2,2,2,4,4,4,4,8,8,8,8,16,16,16,16,32,32,32,32,64,64,64,64,128,128] 

def list_devices():
    # List all audio input devices
    p = pyaudio.PyAudio()
    i = 0
    n = p.get_device_count()
    while i < n:
        dev = p.get_device_info_by_index(i)
        if dev['maxInputChannels'] > 0:
           print(str(i)+'. '+dev['name'])
        i += 1

# Audio setup
no_channels = 1
sample_rate = 44100

# Chunk must be a multiple of 8
# NOTE: If chunk size is too small the program will crash
# with error message: [Errno Input overflowed]
chunk = 4096

list_devices()
# Use results from list_devices() to determine your microphone index
device = 2 

p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16,
                channels = no_channels,
                rate = sample_rate,
                input = True,
                frames_per_buffer = chunk,
                input_device_index = device)


# Return power array index corresponding to a particular frequency
def piff(val):
    return int(2*chunk*val/sample_rate)
   
def calculate_levels(data, chunk,sample_rate):
    global matrix
    # Convert raw data (ASCII string) to numpy array
    data = unpack("%dh"%(len(data)/2),data)
    data = np.array(data, dtype='h')
    # Apply FFT - real data
    fourier=np.fft.rfft(data)
    # Remove last element in array to make it the same size as chunk
    fourier=np.delete(fourier,len(fourier)-1)
    # Find average 'amplitude' for specific frequency ranges in Hz
    power = np.abs(fourier)
    
    matrix[0]= int(np.mean(power[piff(0)   :piff(22):1]))*bassAdj
    matrix[1]= int(np.mean(power[piff(22)    :piff(28):1]))*bassAdj      
    matrix[2]= int(np.mean(power[piff(28)  :piff(36):1]))*bassAdj
    matrix[3]= int(np.mean(power[piff(36)  :piff(44):1]))*bassAdj
    matrix[4]= int(np.mean(power[piff(44)  :piff(56):1]))*bassAdj
    matrix[5]= int(np.mean(power[piff(56)  :piff(70):1]))*bassAdj
    matrix[6]= int(np.mean(power[piff(70) :piff(89):1]))*bassAdj
    matrix[7]= int(np.mean(power[piff(89) :piff(112):1]))*bassAdj
    matrix[8]= int(np.mean(power[piff(112) :piff(141):1]))*bassAdj
    matrix[9]= int(np.mean(power[piff(140):piff(180):1]))*bassAdj
    matrix[10]= int(np.mean(power[piff(178):piff(224):1]))*bassAdj
    matrix[11]= int(np.mean(power[piff(224):piff(282):1]))*midAdj
    matrix[12]= int(np.mean(power[piff(282):piff(355):1]))*midAdj
    matrix[13]= int(np.mean(power[piff(355):piff(447):1]))*midAdj
    matrix[14]= int(np.mean(power[piff(447):piff(562):1]))*midAdj
    matrix[15]= int(np.mean(power[piff(562):piff(622):1]))*midAdj   
    matrix[16]= int(np.mean(power[piff(622):piff(708):1]))*midAdj
    matrix[17]= int(np.mean(power[piff(708):piff(788):1]))*midAdj
    matrix[18]= int(np.mean(power[piff(788):piff(891):1]))*midAdj
    matrix[19]= int(np.mean(power[piff(891):piff(1122):1]))*midAdj
    matrix[20]= int(np.mean(power[piff(1122):piff(1413):1]))*midAdj
    matrix[21]= int(np.mean(power[piff(1413):piff(1778):1]))*midAdj
    matrix[22]= int(np.mean(power[piff(1778):piff(2239):1]))*midAdj
    matrix[23]= int(np.mean(power[piff(2239):piff(2818):1]))*midAdj
    matrix[24]= int(np.mean(power[piff(2818):piff(3548):1]))*midAdj
    matrix[25]= int(np.mean(power[piff(3548):piff(4467):1]))*trebleAdj
    matrix[26]= int(np.mean(power[piff(4467):piff(5623):1]))*trebleAdj
    matrix[27]= int(np.mean(power[piff(5623):piff(7079):1]))*trebleAdj
    matrix[28]= int(np.mean(power[piff(7079):piff(8913):1]))*trebleAdj
    matrix[29]= int(np.mean(power[piff(8913):piff(11220):1]))*trebleAdj

    # Tidy up column values for the LED matrix
    matrix=np.divide(np.multiply(matrix,weighting),1000000)
    # Set floor at 0 and ceiling at 8 for LED matrix
    matrix=matrix.clip(0,sizeY)
    return matrix

# Main loop
while 1:
    try:
        # Get microphone data
        data = stream.read(chunk)
        matrix=calculate_levels(data, chunk,sample_rate)
        strip.clear()
        for y in range (0,30):
            for x in range(0, matrix[y]):
                strip.setPixelColor(pixelGrid[x][y], 255,255,255)
		strip.setPixelColor(pixelGrid[x][y]+1, 255,255,255)
        strip.show()
    except KeyboardInterrupt:
        print("Ctrl-C Terminating...")
        stream.stop_stream()
        stream.close()
        p.terminate()
        sys.exit(1)
    except Exception, e:
        print(e)
        print("ERROR Terminating...")
        stream.stop_stream()
        stream.close()
        p.terminate()
        sys.exit(1)
