'''
Descripttion: 
    1. SPI_CCD principle proof
    2. Single CCD and DMD without turnable machine
version: 2.0.1
    1. 在循环里面进行采集的时候,关注执行完全部的循环花费的时间的多少
Author: luxin
Date: 2024-01-09 15:00:32
LastEditTime: 2024-01-11 17:17:38
Steps:
    1. 原始代码将转台的位置转到合适位置
    2. 用一个成像物体的片作为目标
    3. 先检测裁剪代码的代码有没有什么问题
    4. DMD运行进行同步的内容获取 
    5. image process先处理获取的数据的裁剪/计算裁剪过后的intensity
    
# NOTE: 相机恒定帧率采集代码,注意相机需要初始化的情况
'''

import os
import cv2
import gxipy as gx
from scipy import io
from MyThreadFunc import *
import matplotlib.pyplot as plt
from natsort import natsorted, ns
from ALP4 import *

# --------------------load speckle patterns-------------------
size = 10
ref_path = "D:/Speckle pattern/RandomField_1280-800/070"

os.chdir(ref_path)

filelist = [f for f in os.listdir(ref_path) if f.endswith('.png')]
filelist = natsorted(filelist)

img_data = []
for i in range(size):
    img = cv2.imread(filelist[i], cv2.IMREAD_GRAYSCALE)
    img_data.append(img)
img_data = np.asarray(img_data)

flipped_image = []
for i in range(size):
    img_data[i] = np.flip(img_data[i], axis=1)
    flipped_image.append(img_data[i])
print(len(flipped_image)) 

arr = []
for k in range(size):
    image = img_data[k].flatten()
    arr.append(image)
arr = np.asarray(arr)

# -------------------- signal acquisition-------------------
def acq_mono(device, num):
    global image_lsit
    image_list = []
    path = 'D:/Ghost Imaing Program/python/DMD_Control'
    os.chdir(path)
    DMD = ALP4(version='4.3')
    DMD.Initialize()
    bitDepth = 1
    print(DMD.nSizeX, DMD.nSizeY)
    imgBlack = np.zeros([DMD.nSizeY, DMD.nSizeX])
    DMD.SeqAlloc(nbImg=size, bitDepth=bitDepth)
    DMD.SeqPut(imgData=arr)  
    DMD.SetTiming(illuminationTime=1000000, pictureTime=1000000)
    # define the illuminationTime less than pictureTime(half would be better)
    # 25000 equal to 0.025 second (in 1 second 40 pictures can be printed) X
    # 50000 equal to 0.05 second (in 1 second 20 pictures can be printed) X
    # 100000 equal to 0.1 second (in 1 second 10 pictures can be printed) X
    # 200000 equal to 0.2 second (in 1 second 5 pictures can be printed) O
    #NOTE: Start Acquisition
    # DMD.Run()
    print("DMD working .....")
    Acquisition_start_time = time.perf_counter()
    for i in range(num):
        start_time = time.perf_counter()
        
        device.AcquisitionStart.send_command()
        
        raw_image = device.data_stream[0].get_image()
        if raw_image is None :
            print("Error: get raw image failed")
            continue
        numpy_image = raw_image.get_numpy_array()
        if numpy_image is None:
            print("Error: get numpy image() failed")
            continue
        # NOTE: append numpy image 
        image_list.append(numpy_image)
        
        device.AcquisitionStop.send_command()
        
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print("single acquisition time: {}s".format(elapsed_time))
        # if elapsed_time is not None:
        #     time.sleep(elapsed_time)
        # else:
        #     print("TimeWarning: the for loop time is out range.")
    Acquisition_end_time = time.perf_counter()
    print("The whole acquisition time: {}s".format(Acquisition_end_time - Acquisition_start_time))
    print("Image number", len(image_list))
    print(image_list[0].shape)
    image_process(image_list)
    print("Image process finished .....")
    DMD.Halt()
    DMD.FreeSeq()
    DMD.Free()
    print("DMD closed .....")

def TriggerFunction():
    device_manager = gx.DeviceManager()
    dev_num, dev_info_list = device_manager.update_device_list()
    if dev_num is 0:
        print("Number of enumerated devices is 0")
        return
    cam = device_manager.open_device_by_sn('FCB23030399')
    cam.ExposureTime.set(10000)
    cam.Gain.set(10.0)
    # if dev_info_list[0].get("device_class") == gx.GxDeviceClassList.USB2:
    #     cam.TriggerMode.set(gx.GxSwitchEntry.ON)
    # else:
    #     cam.TriggerMode.set(gx.GxSwitchEntry.ON)
    #     cam.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)
    
    # set the AcquisitionMode
    cam.AcquisitionMode.set(gx.GxAcquisitionModeEntry.CONTINUOUS)
    cam.AcquisitionFrameRateMode.set(gx.GxSwitchEntry.ON)
    cam.AcquisitionFrameRate.set(20.0)
    if cam.AcquisitionFrameRate.is_implemented():
        print("The current AcquisitionRate is " + str(cam.AcquisitionFrameRate.get()))
        
    cam.stream_on()
    print("Camera stream on and working .....")
    
    if cam.PixelColorFilter.is_implemented() is False:
        acq_mono(cam, 10)

    cam.stream_off()
    cam.close_device()
    print("Camera stream off and closed .....")
    # NOTE: image precess

# -------------------- image process -------------------
def image_process(image_list):
    global intensity
    global cropped_image_list
    intensity = []
    if len(image_list) is not None:
        print("The image number is ", len(image_list))
        for i in range(len(image_list)):
            crop_image_anywhere(image_list[i], 1140, 1020, 140, 140, i)    
        if len(intensity) == size and len(image_list) == size:
            # save the cropped_image_list
            folder_capture = "./2024-ConbinedCode/capture"
            if not os.path.exists(folder_capture):
                os.makedirs(folder_capture)
                file_path = os.path.join(folder_capture, 'cropped_image_list.npy')
                try:
                    np.save(file_path, cropped_image_list)
                except Exception as e:
                    print("The '.npy' file unsaved ..... ")
            # save the intensity
            folder_intensity = "./2024-ConbinedCode/capture"
            if not os.path.exists(folder_intensity):
                file_path =os.path.join(folder_intensity, 'list.txt')
                with open(file_path, 'w') as file:
                    for item in intensity:
                        file.write(str(item) + '\n')
                    print('intensity saved successfully! .....')
            DGI(img_data, intensity)
            return intensity

def crop_image_anywhere(numpy_image, x, y, width, height, i):
    # x, y test in specific situation
    global intensity
    global cropped_image_list
    cropped_image_list = []
    cropped_image = numpy_image[y:y + height, x:x + width]
    noise = np.where(cropped_image > 200)
    cropped_image[noise] = 0
    cropped_image_list.append(cropped_image)
    sum = np.sum(cropped_image)
    intensity.append(sum)
    print(sum)
    return

# -------------------- DGI Algorithm -------------------
def DGI(img_data, intensity):
    data = intensity
    bucket = data
    ghost = np.zeros((800, 1280))
    bucket_sum = 0
    sum_field = ghost + 0.00001
    corr_sum = ghost 
    number_sum = 0
    ghost_sum = ghost
    number_sum = 0
    plt.ion()
    
    for i in range(np.size(data)):
        image = img_data[i]
        img = image.astype('float64')
        sum_field = sum_field + img
        number = np.sum(img)
        number_sum = number_sum + number
        mean_number = number_sum/(i+1)
        
        print(i)
        
        # Differential GI 
        mean_field = sum_field / (i + 1)
        bucketDebug = bucket[i]
        bucket_sum = bucket_sum + bucketDebug
        mean_bucket = bucket_sum / (i + 1)
        ghost_sum =ghost_sum + (((img/mean_field) - 1) * (bucketDebug - (mean_bucket * number / mean_number)))
        
        ghost_final = ghost_sum / (i + 1)
        
        if i == size:
            break
    plt.imshow(ghost_final)
    # 将二维矩阵ghost_final保存为图像
    plt.imsave('ghost_final.png', ghost_final)    
    io.savemat('ghost_final.mat', {'data': ghost_final})

# --------------------main-------------------
def main():
    global image_list
    global intensity
    TriggerFunction()

if __name__ == "__main__":
    main()