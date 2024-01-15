import os
import numpy as np
from natsort import natsorted, ns
import matplotlib.pyplot as plt
import time
import cv2
from ConbinedCodeCenter import TriggerFunction


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


# iteration number:1500
size = 1500 


# values is the SPD detection value/intensity value caculated by area array
data = 1 # values 
bucket = data
ghost = np.zeros((800, 1280))
bucket_sum = 0
sum_field = ghost+ 0.00001
corr_sum = ghost
number_sum = 0
ghost_sum = ghost
number_sum=0
plt.ion()

for i in range(np.size(data)):
    
    # img_data[i] == speckle pattern[i]
    image = img_data[i]
    img = image.astype('float64')
    sum_field = sum_field+img
    number = np.sum(img)
    number_sum = number + number_sum
    mean_number = number_sum/(i+1) 
    
        
    print(i)

    # Differential GI
    mean_field = sum_field/(i+1)
    bucketDebug = bucket[i]
    # bucketDebug = bucketDebug[0]
    bucket_sum = bucket_sum+bucketDebug
    mean_bucket = bucket_sum/(i+1)
    ghost_sum =ghost_sum + (((img/mean_field) - 1)*(bucketDebug - (mean_bucket*number/mean_number)))
    # isnan = np.isnan(ghost_sum)
    # print(True in isnan)
    
    ghost_final = ghost_sum/(i+1)

    if i == size:
        break

plt.imshow(ghost_final)

from scipy import io
io.savemat('ghost_final.mat',{'data': ghost_final})