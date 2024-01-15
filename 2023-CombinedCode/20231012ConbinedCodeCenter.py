import os
import cv2
import time 
import random
import gxipy as gx
import numpy as np
from ctypes import *
from PIL import Image
from scipy import io
from MyThreadFunc import *
import matplotlib.pyplot as plt
from natsort import natsorted, ns
from ALP4 import *

# closed loop control signal
openclose = 0

# ---------------------------加载散斑--------------------------
# speckle pattern 
size = 500
#ref_path = "C:/Users/allen/Desktop/intensity patterns/random16"
ref_path = "D:/Speckle pattern/RandomField_1280-800/070"
#ref_path = "C:/Users/allen/Desktop/BesselM0-1J-speckle/BesselM1J-50-s100-5"
#ref_path = "C:/Users/allen/Desktop/intensity patterns/random48"

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

# ----------------------转台控制外部连接库-----------------------
MT_API = windll.LoadLibrary("D:/3D platform/development-H/3D platform program/BasicDemo/MT_API.dll")


# --------------------------转台控制代码-------------------------


def open_zt():
    global error_x
    # 64位系统和32位系统的dll 不一样，注意切换
    MT_API.MT_Open_UART.argtypes = [c_char_p]
    # 初始化转台状态//后面需要释放资源
    MT_API.MT_Init()
    # 直线台19200脉冲转物理量,细分32，直线传动比1，螺距2mm
    MT_API.MT_Help_Step_Line_Steps_To_Real.argtypes = [c_double, c_int32, c_double, c_double, c_int32]
    MT_API.MT_Help_Step_Line_Steps_To_Real.restype = c_double
    fReal = MT_API.MT_Help_Step_Line_Steps_To_Real(1.8, 32, 2, 1, 19200)
    # 旋转台6400脉冲转物理量,细分32，传动比180
    MT_API.MT_Help_Step_Circle_Steps_To_Real.argtypes = [c_double, c_int32, c_double, c_int32]
    MT_API.MT_Help_Step_Circle_Steps_To_Real.restype = c_double
    fReal = MT_API.MT_Help_Step_Circle_Steps_To_Real(1.8, 32, 180, 6400)
    # 直线台2mm物理量转脉冲,细分32，直线传动比1，螺距2mm
    MT_API.MT_Help_Step_Line_Real_To_Steps.argtypes = [c_double, c_int32, c_double, c_double, c_double]
    MT_API.MT_Help_Step_Line_Real_To_Steps.restype = c_int32
    iSteps = MT_API.MT_Help_Step_Line_Real_To_Steps(1.8, 32, 2, 1, 2)
    # 旋转台360°物理量转脉冲,细分32，旋转传动比180
    MT_API.MT_Help_Step_Circle_Real_To_Steps.argtypes = [c_double, c_int32, c_double, c_double]
    MT_API.MT_Help_Step_Circle_Real_To_Steps.restype = c_int32
    iSteps = MT_API.MT_Help_Step_Circle_Real_To_Steps(1.8, 32, 180, 360)

    # 使用USB接口，或者使用串口，或者使用网口
    charPointer = bytes("COM3", "gbk")
    # MT_API.MT_Open_UART("COM8")
    MT_API.MT_Open_UART(charPointer)
    iR = MT_API.MT_Check()
    # iR =0 为成功
    if iR == 0:
        print("iR=", iR)
        print("Rotating device connected successfully")
    else:
        print("Rotating device connected failed")
        # print(obj_cam_operation.img_data)
        # np.savetxt("nimabi.txt",obj_cam_operation.img_data)


def close_zt():
    # 关闭通信口
    MT_API.MT_Close_UART()
    # MT_API.MT_Close_Net()
    # MT_API.MT_Close_USB()
    # DeInit最后调用，释放资源
    MT_API.MT_DeInit()
    print("Turn off rotating devices and free up resources")


def set_zt_initial():
    MT_API.MT_Set_Axis_Halt_All()
    # 设置当前位置为0点 ,也可以设置为任意坐标值，后续坐标对应变化
    MT_API.MT_Set_Axis_Software_P(0, 0)
    MT_API.MT_Set_Axis_Software_P(1, 0)
    MT_API.MT_Set_Axis_Software_P(2, 0)

    # 位置模式 加速度 减速度 最大速度（匀速运行速度）
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

    print("Rotating device Initialized successfully")


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

    # 判断位置相对初始位置的变化大小，超过一定的数量的时候停止电机的工作//默认使用的两个转轴index=0,1
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
    # 恢复初始方向为反向
    # MT_API.MT_Set_Axis_Position_P_Target_Rel(0, -home_control_x)
    # MT_API.MT_Set_Axis_Position_P_Target_Rel(1, -home_control_y)


# zt control template@change the axis
def func(x, y, center, i, num):
    global error_x 
    global error_y
    print("Tracing..............", (x, y))
    error_x = int(x) - center[0]
    error_y = center[1] - int(y)
    if i <= num:
        control_x = int(100 * error_x)
        control_y = int(100 * error_y)
        control_z = control_x
        MT_API.MT_Set_Axis_Position_P_Target_Rel(0, control_x)
        MT_API.MT_Set_Axis_Position_P_Target_Rel(1, control_y)
        MT_API.MT_Set_Axis_Position_P_Target_Rel(2, control_z)


# control axis (0, 1)/(1, 2)
def func1(x, y, center):
    global error_x
    global error_y
    print("Tracing............")
    # if x is not None and y is not None:
    if str(x) != 'nan' and str(y) != 'nan':
        print("Object x axis : %d  Object y axis : %d" % (x, y))
        error_x = float(x) - center[0]
        error_y = center[1] - float(y)
        control_x = int(100 * error_x)
        control_y = int(100 * error_y)
        print("Error x : %d  Error y : %d" % (error_x, error_y))
        print("Control x : %d  Control y : %d" % (control_x, control_y))
    # MT_API.MT_Set_Axis_Position_P_Target_Rel(2, control_x)
    # MT_API.MT_Set_Axis_Position_P_Target_Rel(1, control_y) 
    
    
# additional conditions added
def func3(x, y, center):
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
    for i in range(10):
        device.TriggerSoftware.send_command()
        raw_image = device.data_stream[0].get_image()
        if raw_image is None:
            print("Calibration acqusition image failed ")
            continue
        numpy_image = raw_image.get_numpy_array()
        cxy = np.where(numpy_image >= 255)
        if len(cxy) != 0:
            cx = np.mean(cxy[1])
            cy = np.mean(cxy[0])
            func3(cx, cy, center)
    openclose = 1

# --------------------------相机控制代码-------------------------
# cam2_control_function: image processing
def image_processing(image_list):
    global intensity
    intensity = []
    print(len(image_list))
    for i in range(len(image_list)):
        # acquire_block(image_list[i], 800, 1280, i)
        # crop_image(image_list[i], 160, 160, i)
        crop_image_anywhere(image_list[i], 1140, 1020, 140, 140, i)
    print(image_list[0])
    print(image_list[0].shape)
    print(image)
    print(intensity)
    # save the intensity
    folder_path = "C:/Users/allen/Desktop/Code2/data/intensity"
    store_list_to_folder(intensity, folder_path)
    # # normalization intensity
    # max_value = max(intensity)
    # min_value = min(intensity)
    # print(max_value, min_value)
    # for i in range(len(intensity)):
    #     intensity[i] = (intensity[i] - min_value) / (max_value - min_value)
    # print(intensity)
    # DGI(img_data, intensity)
    DGI(img_data, intensity)
    return intensity 

# Method_1: slice the image
def acquire_block(numpy_image, a, b, i):
    new_image = []
    center = [1223, 1023]
    print("The Width of the Image is:%d  The Height of the Image is:%d"
          % (len(numpy_image[:, 1]), len(numpy_image[0])))
    sx = int(center[0] - a / 2)
    sy = int(center[1] - b / 2)
    # check the position //**这里print的信息最后都可以慢慢删除，测试代码输出是否正确**//
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
    transfer_and_save_single_image(numpy_image, i)
    sum = np.sum(numpy_image)
    intensity.append(sum)
    print(np.sum(numpy_image))
    return

# Method_3: crop image from everywhere you want
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
    save_directory = "C:/Users/allen/Desktop/Code2/data/images"
    os.makedirs(save_directory, exist_ok=True)
    img = Image.fromarray(image, 'L')
    filename = "image_%d.png" % (i + 1)
    img.save(filename, "png")
    img.save(save_directory + filename, "png")
    
# transfer and save the pictures(image_list)
def transfer_and_save_image(image_list):
    # print(Image_list)
    save_directory = "C:/Users/allen/Desktop/Code2/data/intensity"
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

# acquire color picture template
def acq_color(device, num):
    for i in range(num):
        time.sleep(0.1)
        
        device.TriggerSoftware.send_command()
        raw_image = device.data_stream[0].get_image()
        if raw_image is None:
            print("Getting image failed.")
            continue
        rgb_image = raw_image.convert("RGB")
        if rgb_image is None:
            continue
        numpy_image = rgb_image.get_numpy_array()
        if numpy_image is None:
            continue
        
        img = Image.fromarray(numpy_image, 'RGB')
        img.show()
        print("Frame ID: %d   Height: %d   Width: %d"
              % (raw_image.get_frame_id(), raw_image.get_height(), raw_image.get_width()))


# control two devices acquire_mono
def acq_color2(device1, device2, num):
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
        img1 = Image.fromarray(numpy_image1, 'RGB')
        img2 = Image.fromarray(numpy_image2, 'RGB')
        # img1.show()
        # img2.show()
        print("Frame ID: %d   Height: %d   Width: %d"
              % (raw_image1.get_frame_id(), raw_image1.get_height(), raw_image1.get_width()))
        print("Frame ID: %d   Height: %d   Width: %d"
              % (raw_image2.get_frame_id(), raw_image2.get_height(), raw_image2.get_width()))

        
# acquire mono picture template
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


# control two devices to acquire mono
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


# initial the position(@experiment1: testing the glowing letters)
def acq_mono3(device1, device2, num):
    global cx 
    global cy
    # initialize the DMD
    path = 'D:/Ghost Imaing Program/python/DMD_Control'
    os.chdir(path)
    # daq = NIDAQmxInstrument()
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
    image_list = []
    center = np.array([1223, 1023])
    calibration(device1, 10)
    if openclose == 1:
        time.sleep(3)
        DMD.Run()  # @ DMD/cam2 working ...
        start_time_DMD = time.perf_counter()
        for i in range(num):
            # time.sleep(0.05)
            start_time = time.perf_counter()
            device1.TriggerSoftware.send_command()
            device2.TriggerSoftware.send_command()
            raw_image1 = device1.data_stream[0].get_image()
            raw_image2 = device2.data_stream[0].get_image()
            if raw_image1 is None and raw_image2 is None:
                print("Getting image failed.")
                continue
            numpy_image1 = raw_image1.get_numpy_array()
            numpy_image2 = raw_image2.get_numpy_array()
            image_list.append(numpy_image2)
            if numpy_image1 is None and numpy_image2 is None:
                continue
            # cam1 function
            cxy = np.where(numpy_image1 >= 255)
            if len(cxy) != 0:
                cx = np.mean(cxy[1])
                cy = np.mean(cxy[0])
                func3(cx, cy, center)
            else:
                continue
            end_time = time.perf_counter()
            Timeprocedure = end_time - start_time
            if Timeprocedure >= 0:
                time.sleep(Timeprocedure)
            else:
                print("TimeWarning: the for loop time is out range.")
            # print(Timeprocedure)
        end_time_DMD = time.perf_counter()
        Timeprecedure_DMD = end_time_DMD - start_time_DMD
        print(Timeprecedure_DMD)
    print("Image number", len(image_list))
    print(image_list[0].shape)
    # save the image_list 
    '''
        1. Run in image_processing cost too much time
        2. transfer to the cropped_image function 
    '''
    # transfer_and_save_image(image_list)
    DMD.Halt()
    DMD.FreeSeq()
    DMD.Free()
    image_processing(image_list)
    return image_list


# @practice TriggerFunction() //这里只说明之间的逻辑关系
# testing the camera fucntion
def TriggerFunction():
    # create a device manager
    device_manager = gx.DeviceManager()
    dev_num, dev_info_list = device_manager.update_device_list()
    if dev_num is 0:
        print("Number of enumerated devices is 0")
        return
    print(dev_num)  # find the count about device
    print(dev_info_list)  # check the information in dev_info_list
    # # open the first device
    cam1 = device_manager.open_device_by_sn('FCB22070897')
    cam2 = device_manager.open_device_by_sn('FCB23030399')
    # cam1 = device_manager.open_device_by_index(1)
    # cam2 = device_manager.open_device_by_index(2)
    print(dev_info_list[0].get("device_class"))   # 输出的是两个设备列表的字典信息dev_info_list表示的是第一个设备的信息
    print(dev_info_list[1].get("device_class"))   # 输出的是dev_info_list字典结构中的第二个设备的信息
    print(dev_info_list[0].get('sn'), 
          dev_info_list[1].get('sn'))
    print(gx.GxDeviceClassList.USB2)

    # set exposure what does it mean 10000?
    cam1.ExposureTime.set(10000)
    cam2.ExposureTime.set(10000)
    # set gain
    cam1.Gain.set(0.05)     
    cam2.Gain.set(0.05)

    # note the basic information about TriggerMode and TriggerSource
    # if dev_info_list[0].get("device_class") and dev_info_list[1].get("device_class") == gx.GxDeviceClassList.USB2:
    #     # set trigger mode
    #     cam1.TriggerMode.set(gx.GxSwitchEntry.ON)
    #     cam2.TriggerMode.set(gx.GxSwitchEntry.ON)
    # else:
    #     # set trigger mode and trigger source
    #     cam1.TriggerMode.set(gx.GxSwitchEntry.ON)
    #     cam2.TriggerMode.set(gx.GxSwitchEntry.ON)
    #     cam1.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)
    #     cam2.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)

    # start data acquisition
    cam1.stream_on()
    cam2.stream_on()
    print("Camera working ....")
    
    # dedfine the acqusition mode
    cam2.AcquisitionMode.set(gx.GxAcquisitionModeEntry.CONTINUOUS)
    cam2.AcquisitionFrameRateMode.set(gx.GxSwitchEntry.ON)
    cam2.AcquisitionFrameRate.set(20)
    
    # testing the normal capture function
    if cam1.PixelColorFilter.is_implemented() and cam2.PixelColorFilter.is_implemented is True:
        acq_color(cam1, 1)
        # acq_color(cam2, 1)
    # camera is mono camera
    else:
        print("working here ...")
        # test the functionality of both cameras
        # acq_mono2(cam1, cam2, 1)
        # change the cosntruction of acq_mono to another function name and function
        acq_mono3(cam1, cam2, 500)
    cam1.stream_off()
    cam2.stream_off()
    # 这里要测试两个相机是否可以正常工作需要的acq_mono()函数的框架结构，输入两个device


# --------------------------DGI Algorithm-------------------------
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
    
# TurnableAndCam1ControlFunction()    
def TurnableAndCam1ControlFunction():
    center = np.array([1223, 1023])
    device_manager = gx.DeviceManager()
    dev_num, dev_info_list = device_manager.update_device_list()
    cam1 = device_manager.open_device_by_sn('FCB22070897')
    cam1.ExposureTime.set(10000)
    cam1.Gain.set(0.05)
    # define the mode to TriggerMode and TriggerSource
    # cam1.AcquisitionMode.set(gx.GxAcquisitionModeEntry.CONTINUOUS)
    # cam1.AcquisitionFrameRateMode.set(gx.GxSwitchEntry.ON)
    # cam1.AcquisitionFrameRate.set(20.0)
    if dev_info_list[0].get("device_class") == gx.GxDeviceClassList.USB2:
        cam1.TriggerMode.set(gx.GxSwitchEntry.ON)
    else:
        cam1.TriggerMode.set(gx.GxSwitchEntry.ON)
        cam1.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)
    cam1.stream_on()
    for i in range(500):
        cam1.TriggerSoftware.send_command()
        raw_image = cam1.data_stream[0].get_image()
        if raw_image is None: print("Getting image failed.")
        numpy_image = raw_image.get_numpy_array()
        cxy = np.where(numpy_image >= 255)
        if len(cxy) != 0 and str(cxy[0]) != 'nan' and str(cxy[1]) != 'nan':
            cx = np.mean(cxy[1])
            cy = np.mean(cxy[0])
            error_x = float(cx) - center[0]
            error_y = center[1] - float(cy)
            control_x = int(50 * error_x)
            control_y = int(50 * error_y)
            MT_API.MT_Set_Axis_Position_P_Target_Rel(0, control_x)
            MT_API.MT_Set_Axis_Position_P_Target_Rel(1, control_y)
        else:
            print("The cam1 did't capture the target ...........")
            return
    return
 
 
 
# DMDAndCam2AcquisitionFunction()
def DMDAndCam2AcquisitionFunction():
    # initialize the DMD and cam2 device in the same Threading
    path = 'D:/Ghost Imaing Program/python/DMD_Control'
    os.chdir(path)
    # daq = NIDAQmxInstrument()
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
    image_list = []
    device_manager = gx.DeviceManager()
    dev_num, dev_info_list = device_manager.update_device_list()
    cam1 = device_manager.open_device_by_sn('FCB22070897')
    cam1.ExposureTime.set(10000)
    cam1.Gain.set(0.05)
    # define the mode to TriggerMode and TriggerSource
    # NOTE cam1.AcquisitionMode.set(gx.GxSwitchEntry.ON) choose which one ?  
    cam1.AcquisitionMode.set(gx.GxAcquisitionModeEntry.CONTINUOUS)
    cam1.AcquisitionFrameRateMode.set(gx.GxSwitchEntry.ON)
    cam1.AcquisitionFrameRate.set(20.0)
    cam1.stream_on()
    DMD.Run()
    for i in range(500):
        cam1.AcquisitionStart.send_command()
        raw_image = cam1.data_stream[0].get_image()
        if raw_image is None: print("Getting image failed.") 
        numpy_image = raw_image.get_numpy_array()
        image_list.append(numpy_image)
        cam1.AcquisitionStop.send_command()
    print(len(image_list))
    DMD.Halt()
    DMD.FreeSeq()
    DMD.Free()
    cam1.stream_off()
    image_processing(image_list)
    return image_list
    
    

def main():
    global cx
    global cy
    global error_x
    global error_y
    global openclose
    # initialize the turnable
    open_zt()   
    set_zt_initial()
    # add fucntion for calibration
    # calibration() may occuppied the source threading1 using 
    
    # function start
    # TriggerFunction()
    # create threadings to make functions separated
    '''
        1. thread1: turnable control -- cam1 and turnable
         - TurnableAndCam1ControlFunction()
           - open_zt() and set_zt_initial() define befor the threading begin
        2. thread2: acqusition function -- DMD and cam2 device
         - DMDAndCam2AcquisitionFunction()
           - cam2 initialize in the Threading itself as well as DMD initialize
    '''
    thread1 = threading.Thread(target=TurnableAndCam1ControlFunction(), args=())
    thread2 = threading.Thread(target=DMDAndCam2AcquisitionFunction(), args=())
    thread1.start()
    thread2.start()
    print("Waiting for both threads to complete ...........")
    thread1.join()
    thread2.join()
    close_zt()


if __name__ == "__main__":
    main()



        