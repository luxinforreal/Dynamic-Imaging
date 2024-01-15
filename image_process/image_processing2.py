'''
Descripttion: your project
version: 1.0
Author: luxin
Date: 2023-08-15 17:17:09
LastEditTime: 2023-08-19 23:21:19
'''

import cv2
import gxipy as gx
import numpy as np
from ctypes import *
from PIL import Image
from MyThreadFunc import *
import matplotlib.pyplot as plt


# template can not accuratly crop right pictures
# template
def crop_bright_regions(image_path, threshold):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        cropped_image = image[y:y + h, x:x + w]
        cv2.imwrite(f"cropped_{i}.jpg", cropped_image)
        
# crop_bright_regions("image.jpg", 150)


# Plugin for main funtion
def crop_bright_regions1(image, threshold):
    global intensity
    cropped_images = []
    cropped_images_sum = []
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        cropped_image = image[y:y + h, x:x + w]
        print(cropped_image)
        
        noise = np.where(cropped_image >= 100)
        cropped_image[noise] = 0
        cropped_images.append(cropped_image)
        
        sum = np.sum(cropped_image)
        cropped_images_sum.append(sum)
        cv2.imwrite(f"cropped_{i}.jpg", cropped_image)
        # 只存储每次计算得到的最亮的那个散斑对应的图像的大小
    # cropped_images.sort(key=lambda x: x.shape[0] * x.shape[1], reverse=True)
    # cropped_images = sorted(cropped_images, key=lambda x: sum(sum(x, [])), reverse=True)
    cropped_images_sum.sort(reverse=True)
    intensity.append(cropped_images_sum[0])
    print(cropped_images_sum) 


def acq_mono(device, num):
    imagelist = []
    for i in range(num):
        time.sleep(0.1)
        device.TriggerSoftware.send_command()
        raw_image = device.data_stream[0].get_image()
        if raw_image is None:
            print("Getting image failed.")
            continue
        numpy_image = raw_image.get_numpy_array()
        print("Height:", numpy_image.shape[0], "Width:", numpy_image.shape[1])
        imagelist.append(numpy_image)
        if numpy_image is None:
            continue
        # img = Image.fromarray(numpy_image, 'L')
        # img.show()
    print(len(imagelist))
    print(imagelist[0])
    imageprocess(imagelist)


def imageprocess(imagelist):  # 需要重新组织一下代码的架构
    global intensity
    intensity = []
    for i in range(len(imagelist)):
        # 连续获取两张图片看一下裁剪的情况
        # print(np.sum(imagelist[0]))
        crop_bright_regions1(imagelist[i], 1280, 800)
        # sum = np.sum(imagelist[i])
        # intensity.append(sum)
    print(intensity)
    # DGI 
    return


# testing cam1
def testing():
    # create a device manager
    device_manager = gx.DeviceManager()
    dev_num, dev_info_list = device_manager.update_device_list()
    if dev_num is 0:
        print("Number of enumerated devices is 0")
        return
    # cam1 = device_manager.open_device_by_sn('FCB22070897')
    cam2 = device_manager.open_device_by_sn('FCB23030399')
    # cam1 = device_manager.open_device_by_index(1)
    # cam2 = device_manager.open_device_by_index(2)
    cam2.ExposureTime.set(10000)
    cam2.Gain.set(0.05)
    if dev_info_list[0].get("device_class") and dev_info_list[1].get("device_class") == gx.GxDeviceClassList.USB2:
        cam2.TriggerMode.set(gx.GxSwitchEntry.ON)
        # cam2.TriggerMode.set(gx.GxSwitchEntry.ON)
    else:
        cam2.TriggerMode.set(gx.GxSwitchEntry.ON)
        cam2.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)
        # cam2.TriggerMode.set(gx.GxSwitchEntry.ON)
        # cam2.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)
    # start data acquisition
    cam2.stream_on()
    # cam2.stream_on()
    print("working normally")

    if cam2.PixelColorFilter.is_implemented():
        acq_mono(cam2, 10)
    else:
        acq_mono(cam2, 10)

    # cam1.stream_off()
    # cam1.close_device()
    cam2.stream_off()
    cam2.close_device()


if __name__ == "__main__":
    testing()
    # image_path = "C:/Users/luxin/Desktop/Dynamic Tracking Ghost Imaging/image_testing.png"
    # new_width = 1280
    # new_height = 800
    # cropped_array = crop_image(image_path, new_width, new_height)




