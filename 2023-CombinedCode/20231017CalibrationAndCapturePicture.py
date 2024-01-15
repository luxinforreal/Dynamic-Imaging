'''
Descripttion: your project
version: 1.0
Author: luxin
Date: 2023-10-17 21:49:04
LastEditTime: 2023-10-17 22:16:35
'''
import os
import cv2
import gxipy as gx
import numpy as np
from ctypes import *
from PIL import Image
from scipy import io
from MyThreadFunc import *
import matplotlib.pyplot as plt
from natsort import natsorted, ns
from ALP4 import *

openclose = 0
MT_API = windll.LoadLibrary("D:/3D platform/development-H/3D platform program/BasicDemo/MT_API.dll")
def open_zt():
    global error_x
    MT_API.MT_Open_UART.argtypes = [c_char_p]
    MT_API.MT_Init()
    MT_API.MT_Help_Step_Line_Steps_To_Real.argtypes = [c_double, c_int32, c_double, c_double, c_int32]
    MT_API.MT_Help_Step_Line_Steps_To_Real.restype = c_double
    fReal = MT_API.MT_Help_Step_Line_Steps_To_Real(1.8, 32, 2, 1, 19200)
    MT_API.MT_Help_Step_Circle_Steps_To_Real.argtypes = [c_double, c_int32, c_double, c_int32]
    MT_API.MT_Help_Step_Circle_Steps_To_Real.restype = c_double
    fReal = MT_API.MT_Help_Step_Circle_Steps_To_Real(1.8, 32, 180, 6400)
    MT_API.MT_Help_Step_Line_Real_To_Steps.argtypes = [c_double, c_int32, c_double, c_double, c_double]
    MT_API.MT_Help_Step_Line_Real_To_Steps.restype = c_int32
    iSteps = MT_API.MT_Help_Step_Line_Real_To_Steps(1.8, 32, 2, 1, 2)
    MT_API.MT_Help_Step_Circle_Real_To_Steps.argtypes = [c_double, c_int32, c_double, c_double]
    MT_API.MT_Help_Step_Circle_Real_To_Steps.restype = c_int32
    iSteps = MT_API.MT_Help_Step_Circle_Real_To_Steps(1.8, 32, 180, 360)
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
    MT_API.MT_Close_UART()
    # MT_API.MT_Close_Net()
    # MT_API.MT_Close_USB()
    MT_API.MT_DeInit()
    print("Turn off rotating devices and free up resources")
    
def set_zt_initial():
    MT_API.MT_Set_Axis_Halt_All()

    MT_API.MT_Set_Axis_Software_P(0, 0)
    MT_API.MT_Set_Axis_Software_P(1, 0)
    MT_API.MT_Set_Axis_Software_P(2, 0)

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
        if numpy_image is None:
            continue
        cxy = np.where(numpy_image >= 255)
        if len(cxy) != 0:
            cx = np.mean(cxy[1])
            cy = np.mean(cxy[0])
            func(cx, cy, center)
    openclose = 1

def capture(device1, device2, num):
    for i in range(num):
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
        img1.show()
        img2.show()
        # judge the center is the same
        imageprocesscenter(numpy_image1, numpy_image2, 100, 100)
        # define the capture area in the picture
        imageprocessanywhere(numpy_image1, numpy_image2, x, y, w, h)
        
def imageprocessanywhere(image1, image2,x, y, w, h):
        cropped_image1 = image1[y:y+h, x:x+w]
        cropped_image2 = image2[y:y+h, x:x+w]
        img1 = Image.fromarray(cropped_image1, 'L')
        img2 = Image.fromarray(cropped_image2, 'L')
        img1.show()
        img2.show()
        
def imageprocesscenter(image1, image2, new_width, new_height):
    # calculate the discrimination between the center
    center1 = np.where(image1 == 255)
    center2 = np.where(image2 == 255)
    print(center1, center2)
    height = image1.shape[1]
    width = image1.shape[0]
    left = (width - new_width) // 2
    top = (height - new_height) // 2
    right = (width + new_width) // 2
    bottom = (height + new_height) // 2
    numpy_image1 = image1[top:bottom, left:right]
    numpy_image2 = image2[top:bottom, left:right]
    img1 = Image.fromarray(numpy_image1, 'L')
    img2 = Image.fromarray(numpy_image2, 'L')
    img1.show()
    img2.show()

def triggerfunction():
    device_manager = gx.DeviceManager()
    dev_num, dev_info_list = device_manager.update_device_list()
    if dev_num is 0:
        print("Number of enumerated devices is 0")
        return
    cam1 = device_manager.open_device_by_sn('FCB22070897')
    cam2 = device_manager.open_device_by_sn('FCB23030399')
    cam1.ExposureTime.set(10000)
    cam2.ExposureTime.set(10000)
    cam1.Gain.set(0.05)     
    cam2.Gain.set(0.05)
    if dev_info_list[0].get("device_class") and dev_info_list[1].get("device_class") == gx.GxDeviceClassList.USB2:
        cam1.TriggerMode.set(gx.GxSwitchEntry.ON)
        cam2.TriggerMode.set(gx.GxSwitchEntry.ON)
    else:
        cam1.TriggerMode.set(gx.GxSwitchEntry.ON)
        cam2.TriggerMode.set(gx.GxSwitchEntry.ON)
        cam1.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)
        cam2.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)
    cam1.stream_on()
    cam2.stream_on()
    print("Camera working ....")
    capture(cam1, cam2, 1)
    cam1.stream_off()
    cam2.stream_off()
    # 这里要测试两个相机是否可以正常工作需要的acq_mono()函数的框架
      
def main():
    global cx
    global cy
    global error_x
    global error_y
    global openclose
    open_zt()   
    set_zt_initial()
    triggerfunction()
    close_zt()

if __name__ == "__main__":
    main()