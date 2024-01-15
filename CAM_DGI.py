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


import os
import numpy as np
import matplotlib.pyplot as plt
import time
import cv2

data = values
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
    number_sum = number + number_sum
    mean_number = number_sum / (i + 1)

    print(i)

    # Differential GI
    mean_field = sum_field / (i + 1)
    bucketDebug = bucket[i]
    # bucketDebug = bucketDebug[0]
    bucket_sum = bucket_sum + bucketDebug
    mean_bucket = bucket_sum / (i + 1)
    ghost_sum = ghost_sum + (((img / mean_field) - 1) * (bucketDebug - (mean_bucket * number / mean_number)))
    # isnan = np.isnan(ghost_sum)
    # print(True in isnan)

    ghost_final = ghost_sum / (i + 1)

    if i == size:
        break

plt.imshow(ghost_final)
