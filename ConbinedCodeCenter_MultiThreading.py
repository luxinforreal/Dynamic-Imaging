'''
Descripttion: your project
version: 1.0
Author: luxin
Date: 2023-09-15 20:34:31
LastEditTime: 2023-10-12 15:53:19
'''
import os
import cv2
import time
import threading
import gxipy as gx
import numpy as np
import matplotlib.pyplot as plt
from ALP4 import *
from ctypes import *
from PIL import Image
from MyThreadFunc import *
from threading import Timer 
from natsort import natsorted

opeenclose = 0

# ---------------------------Speckle Load----------------------------
size = 500
ref_path = "D:/Speckle pattern/RandomField_1280-800/070"
os.chdir(ref_path)

filelist = [f for f in os.listdir(ref_path) if f.endswith('.png')]
filelist = natsorted(filelist)

# Original image
img_data = []
for i in range(size):
    img = cv2.imread(filelist[i], cv2.IMREAD_GRAYSCALE)
    img_data.append(img)
img_data = np.asarray(img_data)

# Flipped image
flipped_image = []
for i in range(size):
    img_data[i] = np.flip(img_data[i], axis=1)
    flipped_image.append(img_data[i])
print(len(flipped_image))    

# Flattened image
arr = []
for k in range(size):
    image = img_data[k].flatten()
    arr.append(image)
arr = np.asarray(arr)

# ---------------------Load Rotating Platform Lib----------------------
MT_API = windll.LoadLibrary("D:/3D platform/development-H/3D platform program/BasicDemo/MT_API.dll")

# ---------------------Load Rotating Platform Lib----------------------
DMD_path = 'D:/Ghost Imaing Program/python/DMD_Control'

def DMD_initialize():
    global DMD
    path = 'D:/Ghost Imaing Program/python/DMD_Control'
    os.chdir(path)
    DMD = ALP4(version='4.3')
    DMD.Initialize()
    bitDepth = 1
    print(DMD.nSizeX, DMD.nSizeY)
    imgBlack = np.zeros([DMD.nSizeY, DMD.nSizeX])
    DMD.SeqAlloc(nbImg=size, bitDepth=bitDepth)
    DMD.SeqPut(imgData=arr)  # @project the speckle pattern
    DMD.SetTiming(illuminationTime=50000, pictureTime=50000)
    # define the illuminationTime less than pictureTime(half would be better)
    # 25000 equal to 0.025 second (in 1 second 40 pictures can be printed) X
    # 50000 equal to 0.05 second (in 1 second 20 pictures can be printed) X
    # 100000 equal to 0.1 second (in 1 second 10 pictures can be printed) X
    # 200000 equal to 0.2 second (in 1 second 5 pictures can be printed) O
    print("The DMD has been initialized correctly ............")

# ----------------------Rotating Platform Control----------------------
def open_zt():
    global error_x
    # 64x or 32X System depends on different DLL 
    MT_API.MT_Open_UART.argtypes = [c_char_p]
    # Initialize the turntable status //Resources need to be released later
    MT_API.MT_Init()
    # Linear stage 19200 pulses to physical quantities, subdivision 32, linear transmission ratio 1, pitch 2mm
    MT_API.MT_Help_Step_Line_Steps_To_Real.argtypes = [c_double, c_int32, c_double, c_double, c_int32]
    MT_API.MT_Help_Step_Line_Steps_To_Real.restype = c_double
    fReal = MT_API.MT_Help_Step_Line_Steps_To_Real(1.8, 32, 2, 1, 19200)
    # Rotary stage 6400 pulses to physical quantity, subdivision 32, transmission ratio 180
    MT_API.MT_Help_Step_Circle_Steps_To_Real.argtypes = [c_double, c_int32, c_double, c_int32]
    MT_API.MT_Help_Step_Circle_Steps_To_Real.restype = c_double
    fReal = MT_API.MT_Help_Step_Circle_Steps_To_Real(1.8, 32, 180, 6400)
    # Linear table 2mm physical quantity to pulse, subdivision 32, linear transmission ratio 1, pitch 2mm
    MT_API.MT_Help_Step_Line_Real_To_Steps.argtypes = [c_double, c_int32, c_double, c_double, c_double]
    MT_API.MT_Help_Step_Line_Real_To_Steps.restype = c_int32
    iSteps = MT_API.MT_Help_Step_Line_Real_To_Steps(1.8, 32, 2, 1, 2)
    # The rotary table rotates physical quantities 360° to pulse, subdivision 32, rotation transmission ratio 180
    MT_API.MT_Help_Step_Circle_Real_To_Steps.argtypes = [c_double, c_int32, c_double, c_double]
    MT_API.MT_Help_Step_Circle_Real_To_Steps.restype = c_int32
    iSteps = MT_API.MT_Help_Step_Circle_Real_To_Steps(1.8, 32, 180, 360)

    # Use USB interface/serial port/network port
    charPointer = bytes("COM3", "gbk")
    # MT_API.MT_Open_UART("COM8")
    MT_API.MT_Open_UART(charPointer)
    iR = MT_API.MT_Check()
    # iR =0 success
    if iR == 0:
        print("iR=", iR)
        print("Rotating device connected successfully")
    else:
        print("Rotating device connected failed")
        # print(obj_cam_operation.img_data)
        # np.savetxt("nimabi.txt",obj_cam_operation.img_data)


def close_zt():
    # Close communication port//different API
    MT_API.MT_Close_UART()
    # MT_API.MT_Close_Net()
    # MT_API.MT_Close_USB()
    # DeInit is called last to release resources
    MT_API.MT_DeInit()
    print("Turn off rotating devices and free up resources")


def set_zt_initial():
    MT_API.MT_Set_Axis_Halt_All()
    # Set current position to 0 point, also can be set to any coordinate
    MT_API.MT_Set_Axis_Software_P(0, 0)
    MT_API.MT_Set_Axis_Software_P(1, 0)
    MT_API.MT_Set_Axis_Software_P(2, 0)

    # Position mode acceleration deceleration maximum speed 
    MT_API.MT_Set_Axis_Mode_Position(0)
    MT_API.MT_Set_Axis_Position_Acc(0, 60000)
    MT_API.MT_Set_Axis_Position_Dec(0, 60000)
    MT_API.MT_Set_Axis_Position_V_Max(0, 100000)

    MT_API.MT_Set_Axis_Mode_Position(1)
    MT_API.MT_Set_Axis_Position_Acc(1, 60000)
    MT_API.MT_Set_Axis_Position_Dec(1, 60000)
    MT_API.MT_Set_Axis_Position_V_Max(1, 100000)

    MT_API.MT_Set_Axis_Mode_Position(2)
    MT_API.MT_Set_Axis_Position_Acc(2, 60000)
    MT_API.MT_Set_Axis_Position_Dec(2, 60000)
    MT_API.MT_Set_Axis_Position_V_Max(2, 100000)

    print("Rotating device has been Initialized correctly ...........")


def set_zt_limitation():
    global position0
    global position1
    global position2

    iPos0 = c_int32(0)
    pPos0 = pointer(iPos0)
    MT_API.MT_Get_Axis_Software_P_Now(0, pPos0)
    position0 = iPos0.value
    print("iPos=", iPos0)

    iPos1 = c_int32(0)
    pPos1 = pointer(iPos1)
    MT_API.MT_Get_Axis_Software_P_Now(1, pPos1)
    position1 = iPos1.value
    print("iPos=", iPos1)

    iPos2 = c_int32(0)
    pPos2 = pointer(iPos2)
    MT_API.MT_Get_Axis_Software_P_Now(2, pPos2)
    position2 = iPos2.value
    print("iPos=", iPos2)

    # Set Corner threshold
    if position0 >= 200000 or position0 <= -200000 or position1 >= 200000 or position1 <= -200000:
        home_zt()
        
def home_zt(list1, list2):
    time.sleep(3)
    # not mean but sum
    home_control_x = 0
    home_control_y = 0
    for i in range(len(list1)):
        home_control_x += list1[i]
    for j in range(len(list2)):
        home_control_y += list2[j]
    print(home_control_x, home_control_y)
    print(-home_control_x, -home_control_y)
    # Immersive the direction
    # MT_API.MT_Set_Axis_Position_P_Target_Rel(0, -home_control_x)
    # MT_API.MT_Set_Axis_Position_P_Target_Rel(1, -home_control_y)

def func(x, y, center):
    global error_x
    global error_y
    # print("Tracing............")
    # print(center)
    # if x.isnan() is False and y .isnan() is False:
    if str(x) != 'nan' and str(y) != 'nan':
        # print("Object x axis : %d  Object y axis : %d  "
        #       % (x, y))
        error_x = float(x) - center[0]
        error_y = center[1] - float(y)
        control_x = int(50 * error_x)
        control_y = int(50 * error_y)
        # print("Error x : %d  Error y : %d  " % (error_x, error_y))
        # print("Control x : %d  Control y : %d " % (control_x, control_y))
        MT_API.MT_Set_Axis_Position_P_Target_Rel(0, control_x)
        MT_API.MT_Set_Axis_Position_P_Target_Rel(1, control_y)
    else:
        return

# turnable calibration function
def calibration(device, num):
    global openclose
    center = [1223, 1023]
    print("Turnable Calibration ... ")
    for i in range(num):
        device.TriggerSoftware.send_command()
        raw_image = device.data_stream[0].get_image()
        if raw_image is None:
            print("Calibration acqusition image failed ")
            continue
        numpy_image = raw_image.get_numpy_array()
        if numpy_image is None:
            continue
        cxy = np.where(numpy_image >= 255)
        if len(cxy) != 0:
            cx = np.mean(cxy[1])
            cy = np.mean(cxy[0])
            func(cx, cy, center)
    openclose = 1

# ------------------------Image Processing ----------------------------
def image_processing(image_list):
    global intensity
    intensity = []
    print(len(image_list))
    for i in range(len(image_list)):
        # acquire_block(image_list[i], 800, 1280, i)
        crop_image(image_list[i], 1280, 800, i)
    print(image_list[0])
    print(image_list[0].shape)
    print(image)
    print(intensity)
    # save the intensity
    folder_path = "C:/Users/luxin/Desktop/20230912/data/intensity"
    store_list_to_folder(intensity, folder_path)
    # # normalization intensity
    # max_value = max(intensity)
    # min_value = min(intensity)
    # print(max_value, min_value)
    # for i in range(len(intensity)):
    #     intensity[i] = (intensity[i] - min_value) / (max_value - min_value)
    # print(intensity)
    # DGI(img_data, intensity)
    return intensity 

# Method_1: slice the image
def acquire_block(numpy_image, a, b, i):
    new_image = []
    center = [1223, 1023]
    print("The Width of the Image is:%d  The Height of the Image is:%d"
          % (len(numpy_image[:, 1]), len(numpy_image[0])))
    sx = int(center[0] - a / 2)
    sy = int(center[1] - b / 2)
    # check the position
    # print("The start position x:%d The start position y:%d" % (sx, sy))
    new_image = numpy_image[sx:sx + a, sy: sy + b]
    print("The Width of the new Image is:%d  The Height of the nwe Image is:%d"
          % (len(new_image[:, 1]), len(new_image[0])))
    # print(new_image)
    # erase the led 
    xy = np.where(new_image >= 255)
    new_image[xy] = 0
    print(new_image.shape)

# Method_2: cropped image capture 
def crop_image(numpy_image, new_width, new_height, i):
    global intensity
    height = numpy_image.shape[1]
    width = numpy_image.shape[0]
    left = (width - new_width) // 2
    top = (height - new_height) // 2
    right = (width + new_width) // 2
    bottom = (height + new_height) // 2
    numpy_image = numpy_image[top:bottom, left:right]
    # img = Image.fromarray(numpy_image, 'L')
    # # newsize=(100, 100)
    # # img = img.resize(newsize)
    # img.show()
    # erase noise effects//@ 255 / 200 / 100
    noise = np.where(numpy_image > 100)
    numpy_image[noise] = 0
    # transfer single picture and save the image
    transfer_and_save_single_image(numpy_image)
    sum = np.sum(numpy_image)
    intensity.append(sum)
    print(np.sum(numpy_image))
    return

# Method_3: cropped image from aanywhere
def crop_image_anywhere(numpy_image, x, y, width, height, i):
    # x, y test in specific situation
    global intensity
    cropped_image = []
    cropped_image = numpy_image[y:y + height, x:x + width]
    noise = np.where(cropped_image > 200)
    cropped_image[noise] = 0
    transfer_and_save_single_image(numpy_image, i)
    sum = np.sum(cropped_image)
    intensity.append(sum)
    print(sum)
    return

# transfer and save the picture(single image)
def transfer_and_save_single_image(image, i):
    save_directory = "C:/Users/luxin/Desktop/20230912/data/images/"
    os.makedirs(save_directory, exist_ok=True)
    img = Image.fromarray(image, 'L')
    filename = "image_%d.png" % (i + 1)
    img.save(filename, "png")
    img.save
    
# transfer and save the pictures(image list)
def transfer_and_save_image(image_list):
    # print(Image_list)
    save_directory = "C:/Users/luxin/Desktop/20230912/data/images/"
    os.makedirs(save_directory, exist_ok=True)
    for i in range(len(image_list)):
        img = Image.fromarray(image_list[i], 'L')
        filename = "image_%d.png" % (i + 1)
        img.save(filename, "png")
        img.save(save_directory + filename, "png")
        # img.show()

def store_list_to_folder(my_list, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # change the filename by changing the 'list.txt'
    file_path = os.path.join(folder_path, 'list.txt')
    with open(file_path, 'w') as file:
        for item in my_list:
            file.write(str(item) + '\n')


# ------------------------Camera Control ----------------------------
'''
   1. 相机中的操作这里只给出acq_mono的代码示例
   2. 控制单个相机和两个相机的操作函数
'''
def acq_mono(device, num):
    for i in range(num):
        time.sleep(0.1)
        device.TriggerSoftware.send_command()
        raw_image = device.data_stream[0].get_image()
        if raw_image is None:
            print("Getting image failed")
            continue
        numpy_image = raw_image.get_numpy_array()
        if numpy_image is None:
            continue
        img = Image.fromarray(numpy_image, 'L')
        img.show()
        print("Frame ID: %d   Height: %d   Width: %d"
              % (raw_image.get_frame_id(), raw_image.get_height(), raw_image.get_width()))

def acq_mono2(device1, device2, num):
    for i in range(num):
        time.sleep(0.1)
        device1.TriggerSoftware.send_command()
        device2.TriggerSoftware.send_command()
        raw_image1 = device1.data_stream[0].get_image()
        raw_image2 = device2.data_stream[0].get_image()
        if raw_image1 is None and raw_image2 is None:
            print("Getting picture dailed")
            continue
        numpy_image1 = raw_image1.get_numpy_array()
        numpy_image2 = raw_image2.get_numpy_array()
        if numpy_image1 is None and numpy_image2 is None:
            continue
        img1 = Image.fromarray(numpy_image1, 'L')
        img2 = Image.fromarray(numpy_image2, 'L')
        # img1.show()
        # img2.show()
        print("Frame ID: %d   Height: %d   Width: %d"
              % (raw_image1.get_frame_id(), raw_image1.get_height(), raw_image1.get_width()))
        print("Frame ID: %d   Height: %d   Width: %d"
              % (raw_image2.get_frame_id(), raw_image2.get_height(), raw_image2.get_width()))

# previous camera_operation()
# def Camera_initialize():
#     global openclose
#     global cam1, cam2
#     # create a device manager
#     device_manager = gx.DeviceManager()
#     dev_num, dev_info_list = device_manager.update_device_list()
#     if dev_num is 0:
#         print("Number of enumerated devices is 0")
#         return
#     print(dev_num)  # find the count about device
#     print(dev_info_list)  # check the information in dev_info_list
#     # # open the first device
#     cam1 = device_manager.open_device_by_sn('FCB22070897')
#     cam2 = device_manager.open_device_by_sn('FCB23030399')
#     # cam1 = device_manager.open_device_by_index(1)
#     # cam2 = device_manager.open_device_by_index(2)
#     print(dev_info_list[0].get("device_class"))
#     print(dev_info_list[1].get("device_class"))
#     print(dev_info_list[0].get('sn'),
#           dev_info_list[1].get('sn'))
#     print(gx.GxDeviceClassList.USB2)
#
#     # set exposure what does it mean 10000?
#     cam1.ExposureTime.set(10000)
#     cam2.ExposureTime.set(10000)
#     # set gain
#     cam1.Gain.set(0.05)
#     cam2.Gain.set(0.05)
#
#     if dev_info_list[0].get("device_class") and dev_info_list[1].get("device_class") == gx.GxDeviceClassList.USB2:
#         # set trigger mode
#         cam1.TriggerMode.set(gx.GxSwitchEntry.ON)
#         cam2.TriggerMode.set(gx.GxSwitchEntry.ON)
#     else:
#         # set trigger mode and trigger source
#         cam1.TriggerMode.set(gx.GxSwitchEntry.ON)
#         cam2.TriggerMode.set(gx.GxSwitchEntry.ON)
#         cam1.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)
#         cam2.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)
#
#     # start data acquisition
#     cam1.stream_on()
#     cam2.stream_on()
#     print("Camera has been initialized correctly ...........")
#
#     # testing the normal capture function
#     if cam1.PixelColorFilter.is_implemented() and cam2.PixelColorFilter.is_implemented is True:
#         openclose = 0
#     else:
#         print("Camera start working here ...")
#         calibration(cam1, 5)
#         openclose = 1

    
# ------------------------Threadinga Operations -------------------------

def dmd_operation():
    global DMD
    path = 'D:/Ghost Imaing Program/python/DMD_Control'
    os.chdir(path)
    DMD = ALP4(version='4.3')
    DMD.Initialize()
    bitDepth = 1
    print(DMD.nSizeX, DMD.nSizeY)
    imgBlack = np.zeros([DMD.nSizeY, DMD.nSizeX])
    DMD.SeqAlloc(nbImg=size, bitDepth=bitDepth)
    DMD.SeqPut(imgData=arr)  # @project the speckle pattern
    DMD.SetTiming(illuminationTime=50000, pictureTime=50000)
    # define the illuminationTime less than pictureTime(half would be better)
    # 25000 equal to 0.025 second (in 1 second 40 pictures can be printed) X
    # 50000 equal to 0.05 second (in 1 second 20 pictures can be printed) X
    # 100000 equal to 0.1 second (in 1 second 10 pictures can be printed) X
    # 200000 equal to 0.2 second (in 1 second 5 pictures can be printed) O
    print("The DMD has been initialized correctly ............")
    # excute the cam2_operation 0.05s pause
    # time.sleep(0.05)
    DMD.Run()
    # DMD.Halt()
    # DMD.FreeSeq()
    # DMD.Free()
    return 

def cam1_operation(num):
    global cam1
    start_time = time.perf_counter()
    center = np.array([1223, 1023])
    # initialize the cam1 in the thread
    device_manager = gx.DeviceManager()
    dev_num, dev_info_list = device_manager.update_device_list()
    if dev_num is 0:
        print("Number of enumerated devices is 0")
        return
    print(dev_info_list[0].get('sn'))
    cam1 = device_manager.open_device_by_sn('FCB22070897')
    cam1.ExposureTime.set(10000)
    cam1.Gain.set(0.05)
    if dev_info_list[0].get("device_class") == gx.GxDeviceClassList.USB2:
        cam1.TriggerMode.set(gx.GxSwitchEntry.ON)
    else:
        cam1.TriggerMode.set(gx.GxSwitchEntry.ON)
        cam1.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)
    cam1.stream_on()
    end_time = time.perf_counter()
    print(end_time - start_time)
    for i in range(num):
        cam1.TriggerSoftware.send_command()
        raw_image = cam1.data_stream[0].get_image()
        if raw_image is None:
            print("Getting image failed")
            continue
        numpy_image = raw_image.get_numpy_array()
        if numpy_image is None:
            continue
        cxy = np.where(numpy_image >= 255)
        if len(cxy) != 0:
            cx = np.mean(cxy[1])
            cy = np.mean(cxy[0])
            global error_x
            global error_y
            # print("Tracing............")
            # print(center)
            # if x.isnan() is False and y .isnan() is False:
            if str(cx) != 'nan' and str(cy) != 'nan':
                # print("Object x axis : %d  Object y axis : %d  "
                #       % (x, y))
                error_x = float(cx) - center[0]
                error_y = center[1] - float(cy)
                control_x = int(50 * error_x)
                control_y = int(50 * error_y)
                # print("Error x : %d  Error y : %d  " % (error_x, error_y))
                # print("Control x : %d  Control y : %d " % (control_x, control_y))
                MT_API.MT_Set_Axis_Position_P_Target_Rel(0, control_x)
                MT_API.MT_Set_Axis_Position_P_Target_Rel(1, control_y)
            else:
                return
        else:
            print("The cam1 did't capture the target ...........")
            continue
    return 


# 添加计数器的版本
def cam2_operation(device):
    '''
        1. directly use the threading.Timer(time, function)
        2. function cam2_operation(device, num) capture picture every 0.05 seconds
        3. wheather it need to be in the a for loop?
    '''
    global counter
    global image_list
    counter = 0
    image_list = []

    device.TriggerSoftware.send_command()
    raw_image = device.data_stream[0].get_image()
    if raw_image is None:
        print("Getting image failed")
    numpy_image = raw_image.get_numpy_array()
    if numpy_image is None:
        print("Getting numpy failed")
    image_list.append(numpy_image)
    
    counter = counter + 1
    if counter < 500:
        t = Timer(0.05, cam2_operation)   
        t.start()
    return

# 非添加计数器版本
def cam2_operation1(num):
    global counter
    global image_list
    counter = 0
    image_list = []

    device_manager = gx.DeviceManager()
    dev_num, dev_info_list = device_manager.update_device_list()
    if dev_num is 0:
        print("Number of enumerated devices is 0")
        return
    print(dev_info_list[0].get('sn'))
    cam2 = device_manager.open_device_by_sn('FCB23030399')
    cam2.ExposureTime.set(10000)
    cam2.Gain.set(0.05)
    if dev_info_list[0].get("device_class") == gx.GxDeviceClassList.USB2:
        cam2.TriggerMode.set(gx.GxSwitchEntry.ON)
    else:
        cam2.TriggerMode.set(gx.GxSwitchEntry.ON)
        cam2.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)
    cam2.stream_on()

    for i in range(num):
        cam2.TriggerSoftware.send_command()
        raw_image = cam2.data_stream[0].get_image()
        if raw_image is None:
            print("Getting image failed")
            continue
        numpy_image = raw_image.get_numpy_array()
        if numpy_image is None:
            print("Getting numpy failed")
            continue
        image_list.append(numpy_image)
# ------------------------Free Hardware Sources -------------------------   
def free_sources():
    # free the turnable 
    close_zt()
    # free the DMD sources
    DMD.Halt()
    DMD.FreeSeq()
    DMD.Free()
    # free the camera sources
    cam1.stream_off()
    cam2.stream_off()
    print("All the device sources has been released")
    
# -----------------------------DGI Algorithm------------------------------
def DGI(img_data, data):
    bucket = data
    ghost = np.zeros((800, 1280))
    bucket_sum = 0
    sum_field = ghost + 0.00001
    corr_sum = ghost
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
        mean_field = sum_field/(i+1)
        bucketDebug = bucket[i]
        # bucketDebug = bucketDebug[0]
        bucket_sum = bucket_sum + bucketDebug
        mean_bucket = bucket_sum/(i+1)
        ghost_sum =ghost_sum + (((img/mean_field) - 1)*(bucketDebug - (mean_bucket*number/mean_number)))
        # isnan = np.isnan(ghost_sum)
        # print(True in isnan)

    
        ghost_final = ghost_sum/(i+1)        
        
        if i == size:
            break
    
    plt.imshow(ghost_final, 2)
    plt.show()
    plt.pause(100)
    plt.savefig('temp.png')
    image_resized = Image.open('temp.png')
    image_resized = image_resized.resize((64, 64))
    image_resized.save('resiezed_image.png')
    image_resized.show()
    # ghost_final = Image.fromarray(ghost_final, 'L')
    # ghost_final = ghost_final.resize((64, 64))
    # image.save("./data/image/20230907ghost.png")
    # io.savemat('ghost_final.mat', {'data': ghost_final})
    
    

def main():
    '''
    - global openclose用于给相机闭环提供信号量
    1. 完成所有设备的初始化工作,转台,相机1.2
    2. 分析出其中最小的测试工作、分别是
        DMD投影散斑到目标位置上
        cam1获取位置进行跟瞄的测试
        cam2获取图像的信息存储他们到image_list里面,这里的image_list设置为全局变量,仅仅作为图像信息的变量名
    '''
    # create the threads
    '''
        1. thread1: define the DMD operation
        2. thread2: define the Cam1 operation
        3. thread3: define the Cam2 operation
    '''
    # thread1 = threading.Thread(target=dmd_operation, args=())
    # thread2 = threading.Thread(target=cam1_operation, args=(500, ))
    # thread3 = threading.Timer(0.05, cam2_operation, args=(cam2,))
    # thread3 = threading.Thread(target=cam2_operation, args=(cam2, 500))
    # thread3 = threading.Timer(0.05, cam2_operation, args=(cam2, 500))
    # thread3 = threading.Thread(target=cam2_operation1, args=(100, ))


    # thread1.start()
    # thread2.start()
    # thread3.start()

    # Wait for both threads to complete
    # 依次检验线程池中的线程是否结束，没有结束就阻塞直到线程结束，如果结束则跳转执行下一个线程的join函数
    print("Waiting for both threads to complete ...........")
    # thread1.join()
    # thread2.join()
    # thread3.join()
    
    # release the sources
    # free_sources()
    

if __name__ == "__main__":
    main()

