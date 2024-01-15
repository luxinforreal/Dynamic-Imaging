'''
Descripttion: Camera Control
version: 1.0
Author: luxin
Date: 2023-06-13 15:30:57
LastEditTime: 2023-08-27 15:34:29
'''
import random
import gxipy as gx
import numpy as np
from ctypes import *
from PIL import Image
from MyThreadFunc import *
import matplotlib.pyplot as plt

# This file is used for testing the camera function


def acq_color(device, num):
    """
           :brief      acquisition function of color device
           :param      device:     device object[Device]
           :param      num:        number of acquisition images[int]
    """
    for i in range(num):
        time.sleep(0.1)

        # send software trigger command
        device.TriggerSoftware.send_command()

        # get raw image
        raw_image = device.data_stream[0].get_image()
        if raw_image is None:
            print("Getting image failed.")
            continue

        # get RGB image from raw image
        rgb_image = raw_image.convert("RGB")
        if rgb_image is None:
            continue

        # create numpy array with data from raw image
        numpy_image = rgb_image.get_numpy_array()
        if numpy_image is None:
            continue

        # show acquired image
        img = Image.fromarray(numpy_image, 'RGB')
        img.show()

        # print height, width, and frame ID of the acquisition image
        print("Frame ID: %d   Height: %d   Width: %d"
              % (raw_image.get_frame_id(), raw_image.get_height(), raw_image.get_width()))


def acq_mono(device, num):
    """
           :brief      acquisition function of mono device
           :param      device:     device object[Device]
           :param      num:        number of acquisition images[int]
    """
    for i in range(num):
        time.sleep(0.1)
        # send software trigger command
        device.TriggerSoftware.send_command()
        # get raw image
        raw_image = device.data_stream[0].get_image()
        if raw_image is None:
            print("Getting image failed.")
            continue
        # create numpy array with data from raw image
        numpy_image = raw_image.get_numpy_array()
        if numpy_image is None:
            continue
        # show acquired image
        img = Image.fromarray(numpy_image, 'L')
        img.show()
        # print height, width, and frame ID of the acquisition image
        print("Frame ID: %d   Height: %d   Width: %d"
              % (raw_image.get_frame_id(), raw_image.get_height(), raw_image.get_width()))

# crop image
def crop_image1(numpy_image, new_width, new_height):
    global intensity
    height = numpy_image.shape[1]
    width = numpy_image.shape[0]
    left = (width - new_width) // 2
    top = (height - new_height) // 2
    right = (width + new_width) // 2
    bottom = (height + new_height) // 2
    numpy_image = numpy_image[top:bottom, left:right]
    img = Image.fromarray(numpy_image, 'L')
    img.show()
    ar, count = np.unique(numpy_image, return_counts=True)
    print(ar, count)
    plt.plot(range(len(ar)), count, 'b')
    plt.show()
    return

# 控制两个相机的获取照片//测试结果：获取照片功能正常
def acq_mono_practice(device1, device2, num):
    for i in range(num):
        time.sleep(0.1)
        start = time.perf_counter()
        device1.TriggerSoftware.send_command()
        device2.TriggerSoftware.send_command()
        raw_image1 = device1.data_stream[0].get_image()
        raw_image2 = device2.data_stream[0].get_image()
        if raw_image1 is None and raw_image2 is None:
            print("Getting picture dailed")
            continue
        numpy_image1 = raw_image1.get_numpy_array()
        numpy_image2 = raw_image2.get_numpy_array()
        ##caculate the distribution of numpy_image1 and numpy_image2
        # ar1, count1 = np.unique(numpy_image1, return_counts=True)
        # ar2, count2 = np.unique(numpy_image2, return_counts=True)
        # print(ar1, count1, ar2, count2)
        # plt.plot(range(len(ar1)), count1, 'b')
        # plt.show()
        # plt.plot(range(len(ar2)), count2, 'r')
        # plt.show()
        if numpy_image1 is None and numpy_image2 is None:
            continue
        img1 = Image.fromarray(numpy_image1, 'L')
        img2 = Image.fromarray(numpy_image2, 'L')
        img1.show()
        img2.show()
        crop_image1(numpy_image2)
        print("Frame ID: %d   Height: %d   Width: %d"
              % (raw_image1.get_frame_id(), raw_image1.get_height(), raw_image1.get_width()))
        print("Frame ID: %d   Height: %d   Width: %d"
              % (raw_image2.get_frame_id(), raw_image2.get_height(), raw_image2.get_width()))
        end = time.perf_counter()
        Timeprocedure = end - start
        print(Timeprocedure)


# 实际应用时候的TriggerFunction软触发函数/在此函数内集成
def TriggerFunction():
    # print the demo information
    print("")
    print("-------------------------------------------------------------")
    print("Sample to show how to acquire mono or color image by soft trigger "
          "and show acquired image.")
    print("-------------------------------------------------------------")
    print("")
    print("Initializing......")
    print("")

    # create a device manager
    device_manager = gx.DeviceManager()
    dev_num, dev_info_list = device_manager.update_device_list()
    if dev_num is 0:
        print("Number of enumerated devices is 0")
        return
    print(dev_num)  # find the count about device
    print(dev_info_list)  # check the information in dev_info_list
    # open the first device //这里使用index的方法是否不够合理应该使用它们自身的唯一标识来确定相机的名称#
    cam1 = device_manager.open_device_by_index(1)
    cam2 = device_manager.open_device_by_index(2)
    # set exposure what does it mean 10000?
    cam1.ExposureTime.set(10000)
    cam2.ExposureTime.set(10000)
    # set gain
    cam1.Gain.set(0.05)  #设置拍摄的间隔，帧率
    cam2.Gain.set(0.05)

# test before the
    if dev_info_list[0].get("device_class") and dev_info_list[1].get("device_class") == gx.GxDeviceClassList.USB2:
        # set trigger mode
        cam1.TriggerMode.set(gx.GxSwitchEntry.ON)
        cam2.TriggerMode.set(gx.GxSwitchEntry.ON)
    else:
        # set trigger mode and trigger source
        cam1.TriggerMode.set(gx.GxSwitchEntry.ON)
        cam2.TriggerMode.set(gx.GxSwitchEntry.ON)
        cam1.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)
        cam2.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)

    # start data acquisition
    cam1.stream_on()
    cam2.stream_on()

    # camera is color camera
    if cam1.PixelColorFilter.is_implemented() and cam2.PixelColorFilter.is_implemented is True:
        acq_color(cam1, 1)
        acq_color(cam2, 1)
    # camera is mono camera
    else:
        # testing the camera is ok
        acq_mono_practice(cam1, cam2, 1)
        # change the cosntruction of acq_mono to another function name and function 

    # stop acquisition
    cam1.stream_off()
    cam2.stream_off()

    # close device
    cam1.close_device()
    cam2.close_device()


# testing the camera fucntion
def testing():
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
    print(dev_info_list[1].get("device_class"))   # 输出的是第二个设备的信息
    print(dev_info_list[0].get('sn'), dev_info_list[1].get('sn'))
    print(gx.GxDeviceClassList.USB2)

    # set exposure what does it mean 10000?
    cam1.ExposureTime.set(10000)
    cam2.ExposureTime.set(10000)
    # set gain
    cam1.Gain.set(0.05)     # 设置拍摄的间隔，帧率
    cam2.Gain.set(0.05)

    # test before the
    if dev_info_list[0].get("device_class") and dev_info_list[1].get("device_class") == gx.GxDeviceClassList.USB2:
        # set trigger mode
        cam1.TriggerMode.set(gx.GxSwitchEntry.ON)
        cam2.TriggerMode.set(gx.GxSwitchEntry.ON)
    else:
        # set trigger mode and trigger source
        cam1.TriggerMode.set(gx.GxSwitchEntry.ON)
        cam2.TriggerMode.set(gx.GxSwitchEntry.ON)
        cam1.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)
        cam2.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)

    # start data acquisition
    cam1.stream_on()
    cam2.stream_on()
    print("working normally")

    # testing the normal capture function
    if cam1.PixelColorFilter.is_implemented() and cam2.PixelColorFilter.is_implemented is True:
        acq_color(cam1, 1)
        acq_color(cam2, 1)
    # camera is mono camera
    else:
        acq_mono_practice(cam1, cam2, 1)
        # change the cosntruction of acq_mono to another function name and function

    cam1.stream_off()
    cam2.stream_off()
    # 这里要测试两个相机是否可以正常工作需要的acq_mono()函数的框架结构，输入两个device


if __name__ == "__main__":
    testing()
    # TriggerFunction()
