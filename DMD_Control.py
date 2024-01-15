import os
from natsort import natsorted, ns
import numpy as np
import cv2
import Conbined_code

size = 1500 

#ref_path = "C:/Users/allen/Desktop/intensity patterns/random16"
ref_path = "D:/Ghost Imaing Program/RandomField_1280-800/064"
#ref_path = "C:/Users/allen/Desktop/BesselM0-1J-speckle/BesselM1J-50-s100-5"

##ref_path = "C:/Users/allen/Desktop/intensity patterns/random48"

os.chdir(ref_path)

filelist = [f for f in os.listdir(ref_path) if f.endswith('.png')]
filelist = natsorted(filelist)

img_data = []
for i in range(size):
    img = cv2.imread(filelist[i], cv2.IMREAD_GRAYSCALE)
    img_data.append(img)
img_data = np.asarray(img_data)

arr = []
for k in range(size):
    image = img_data[k].flatten()
    arr.append(image)
arr = np.asarray(arr)


from ALP4 import *
import time
from daqmx import NIDAQmxInstrument, AnalogInput

path = 'D:/Ghost Imaing Program/python/DMD_Control'
os.chdir(path)

daq = NIDAQmxInstrument()

# Load the Vialux .dll
DMD = ALP4(version = '4.3')
# Initialize the device
DMD.Initialize()

# data = []

# Binary amplitude image (0 or 1)
bitDepth = 1    
imgBlack = np.zeros([DMD.nSizeY, DMD.nSizeX])
# imgWhite = np.ones([DMD.nSizeY,DMD.nSizeX])*(2**8-1)
# imgSeq  = np.concatenate([imgBlack.ravel(),imgWhite.ravel()])
# img_Seq  = np.concatenate([img_data[0].ravel(),img_data[1].ravel(),img_data[2].ravel(),
#                            img_data[3].ravel(),img_data[4].ravel(),img_data[5].ravel(),
#                            img_data[6].ravel(),img_data[7].ravel(),img_data[8].ravel(),
#                            img_data[9].ravel()])

# Allocate the onboard memory for the image sequence (nbImg = number of sequence img)
DMD.SeqAlloc(nbImg = size, bitDepth = bitDepth)
# Send the image sequence as a 1D list/array/numpy array
# DMD.SeqPut(imgData = imgSeq)
DMD.SeqPut(imgData = arr)
# Set image rate to 50 Hz (50 Hz is 50 frame in 1 second)(= 20000 microsecond)
DMD.SetTiming(pictureTime = 50000) 
# 25000 equal to 0.025 second (in 1 second 40 pictures can be printed) X
# 50000 equal to 0.05 second (in 1 second 20 pictures can be printed) X
# 100000 equal to 0.1 second (in 1 second 10 pictures can be printed) X
# 200000 equal to 0.2 second (in 1 second 5 pictures can be printed) O

# Time between the start of two consecutive picture, up to 10^7 microseconds = 10 seconds.
print("start")
# Run the sequence in an infinite loop
DMD.Run()

values = daq.ai0.capture(
    sample_count=1500, rate=20,
    max_voltage=10.0, min_voltage=0,
    # mode='differential', 
    timeout=75.0 #75@1500 100@2000
    )

for i in range(3,0,-1):
    print(f"{i}", end="\r", flush=True)
    time.sleep(1)    # time.sleep(1) means 1 second

DMD.Halt() # Stop the sequence display
DMD.FreeSeq() # Free the sequence from the onboard memory
DMD.Free() # De-allocate the device