'''
Descripttion: test the AcquisitionMode 
version: 1.0
Author: luxin
Date: 2024-01-10 17:38:52
LastEditTime: 2024-01-11 09:46:40
'''
# version:1.0.1905.9071
import gxipy as gx
import time
from PIL import Image


def acq_color(device, num):
    """
           :brief      acquisition function of color device
           :param      device:     device object[Device]
           :param      num:        number of acquisition images[int]
    """
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


def acq_mono(device, num):
    """
           :brief      acquisition function of mono device
           :param      device:     device object[Device]
           :param      num:        number of acquisition images[int]
    """
    global image_list 
    image_list = []
    if device.AcqusititonMode.is_implemented() and device.AcquisitionMode.get() == gx.GxAcquisitionModeList.CONTINUOUS:
        for i in range(num):
            device.AcquisitionStart.send_command()
            raw_image = device.data_stream[0].get_image()
            if raw_image is None:
                print("Getting raw image failed .....")
                continue
            numpy_image = raw_image.get_numpy_array()
            if numpy_image is None:
                print("Getting numpy image failed .....")
                continue
            image_list.append(numpy_image)
            device.AcquisitionStop.send_command()
        print(len(image_list))
        print(image_list[0])
    else:
        print("Acquisition mode is not supported.")
        return            

def main():
    print("")
    print("-------------------------------------------------------------")
    print("Sample to show how to acquire mono or color image by soft trigger "
          "and show acquired image.")
    print("-------------------------------------------------------------")
    print("")
    print("Initializing......")
    print("")

    device_manager = gx.DeviceManager()
    dev_num, dev_info_list = device_manager.update_device_list()
    if dev_num is 0:
        print("Number of enumerated devices is 0")
        return
    cam = device_manager.open_device_by_index(1)
    cam.Gain.set(10.0)
    if dev_info_list[0].get("device_class") == gx.GxDeviceClassList.USB2:
        cam.TriggerMode.set(gx.GxSwitchEntry.ON)
    else:
        cam.TriggerMode.set(gx.GxSwitchEntry.ON)
        cam.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)
        
    cam.AcquisitionMode.set(gx.GxAcquisitionModeEntry.CONTINUOUS)
    cam.AcquisitionFrameRateMode.set(gx.GxSwitchEntry.ON)
    cam.AcquisitionFrameRate.set(20.0)
    if cam.AcquisitionFrameRate.is_implemented():
        print("The current AcquisitonRate is " + cam.AcquisitionFrameRate.get())
    
    cam.stream_on()

    if cam.PixelColorFilter.is_implemented() is True:
        acq_color(cam, 1)
    else:
        acq_mono(cam, 1)

    cam.stream_off()
    cam.close_device()


if __name__ == "__main__":
    main()
