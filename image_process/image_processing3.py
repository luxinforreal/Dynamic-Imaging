'''
Descripttion: test calibration correctly or not
version: 1.0
Author: luxin
Date: 2024-01-09 20:43:57
LastEditTime: 2024-01-09 21:13:50
'''
import gxipy as gx
import numpy as np
from ctypes import *
from PIL import Image
from MyThreadFunc import *
import matplotlib.pyplot as plt


def crop_image_anywhere(numpy_image, x, y, width, height, i):
    # x, y test in specific situation
    global intensity
    intensity = []
    sum1 = np.sum(numpy_image)
    cropped_image = []
    cropped_image = numpy_image[y:y + height, x:x + width]
    noise = np.where(cropped_image > 200)
    cropped_image[noise] = 0
    img = Image.fromarray(cropped_image, 'L')
    img.show()
    time.sleep(5)
    sum2 = np.sum(cropped_image)
    if sum1 == sum2:
        print("The image is not captured correctly!")
        return 
    else: 
        intensity.append(sum)
    print(intensity)
    return


def testing():
    # create a device manager
    device_manager = gx.DeviceManager()
    dev_num, dev_info_list = device_manager.update_device_list()
    if dev_num is 0:
        print("Number of enumerated devices is 0")
        return
    cam2 = device_manager.open_device_by_sn('FCB23030399')
    cam2.ExposureTime.set(10000)
    cam2.Gain.set(10.0)
    if dev_info_list[0].get("device_class") == gx.GxDeviceClassList.USB2:
        cam2.TriggerMode.set(gx.GxSwitchEntry.ON)
    else:
        cam2.TriggerMode.set(gx.GxSwitchEntry.ON)
        cam2.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)
    # start data acquisition
    cam2.stream_on()
    
    if cam2.PixelColorFilter.is_implemented() is False:
        for i in range(1):
            cam2.TriggerSoftware.send_command()
            raw_image = cam2.data_stream[0].get_image()
            if raw_image is None:
                print("Get image failed")
                continue
            numpy_image = raw_image.get_numpy_array()
            if numpy_image is None:
                continue
            img = Image.fromarray(numpy_image, 'L')
            img.show()
            # cropped image
            crop_image_anywhere(numpy_image, 1140, 1020, 140, 140, i)
        
    cam2.stream_off()
    cam2.close_device()

if __name__ == "__main__":
    testing()