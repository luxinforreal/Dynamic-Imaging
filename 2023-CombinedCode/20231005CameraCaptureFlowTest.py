import threading
from PIL import Image
import gxipy as gx
import matplotlib.pyplot as plt

'''
    The following class method are going to be used in this snippet:
    1. self.AcquisitionMode
    2. self.AcquisitionStart
    3. self.AcquisitionStop
    4. self.AcquisitionFrameRateMode
    5. self.AcquisitionFrameRate
    The following class method are used in this snippet:
    1. self.ExposureTime
    2. self.Gain
    3. self.TriggerMode
    4. self.TriggerSource
    5. self.PixelColorFilter
    6. self.stream_on
    7. self.stream_off
'''
# use the trigger mode to acquire image - software trigger
def InitializeAndTestDevice():
    device_manager = gx.DeviceManager()
    dev_num, dev_info_list = device_manager.update_device_list()
    if dev_num is 0:
        print("Number of enumerated devices is 0")
        return
    cam = device_manager.open_device_by_sn('FCB23030399')
    cam.ExposureTime.set(10000.0)
    cam.Gain.set(0.05)
    if dev_info_list[0].get("device_class") == gx.GxDeviceClassList.USB2:
        cam.TriggerMode.set(gx.GxSwitchEntry.ON)
    else:
        cam.TriggerMode.set(gx.GxSwitchEntry.ON)
        cam.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)
    # define the acquisition mode
    # gx.GxAcquisitionModeEntry.SINGLE_FRAME/MULITI_FRAME/CONTINUOUS
    # cam.AcquisitionMode.set(gx.GxAcquisitionModeEntry.CONTINUOUS)
    # cam.AcquisitionFrameRateMode.set(gx.GxSwitchEntry.ON)
    # cam.AcquisitionFrameRate.set(20.0)
    # cam.AcquisitionStart.send_command()
    # cam.AcquisitionStop.send_command()
    print("The current acquisition rate is", cam.CurrentAcquisitionFrameRate)
    cam.stream_on()
    if cam.PixelColorFilter.is_implemented() is False:
        print("This is a Mono camera.")
        for i in range(10):
            print(i)
            cam.TriggerSoftware.send_command()
            raw_image = cam.data_stream[0].get_image()
            if raw_image is None:
                print("Getting image failed.")
                continue    
            numpy_image = raw_image.get_numpy_array()
            if numpy_image is None:
                print("The" + i + "th image is None.")
            image_list.append(numpy_image)
        print(len(image_list))
        img = Image.fromarray(image_list[3], 'L')
        img.show()
    else:
        print("The camera is not Color camera.")
    cam.stream_off()


# use the AcquisitionStart and AcquisitionStop to acquire image
def InitializeAndTestDeviceAcquisitionMode():
    device_manager = gx.DeviceManager()
    dev_num, dev_info_list = device_manager.update_device_list()
    if dev_num is 0:
        print("Number of enumerated devices is 0")
        return
    cam = device_manager.open_device_by_sn('FCB23030399')
    cam.ExposureTime.set(10000.0)
    cam.Gain.set(0.05)
    # if dev_info_list[0].get("device_class") == gx.GxDeviceClassList.USB2:
    #     cam.TriggerMode.set(gx.GxSwitchEntry.ON)
    # else:
    #     cam.TriggerMode.set(gx.GxSwitchEntry.ON)
    #     cam.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)
    # define the acquisition mode
    # gx.GxAcquisitionModeEntry.SINGLE_FRAME/MULITI_FRAME/CONTINUOUS
    cam.AcquisitionMode.set(gx.GxAcquisitionModeEntry.CONTINUOUS)
    cam.AcquisitionFrameRateMode.set(gx.GxSwitchEntry.ON)
    cam.AcquisitionFrameRate.set(20.0)
    print("The current acquistion rate is", cam.CurrentAcquisitionFrameRate)
    cam.stream_on()
    if cam.PixelColorFilter.is_implemented() is False:
        print("This is a Mono camera.")
        # cam.AcquisitionStart.send_command()
        for i in range(10):
            print(i)
            cam.AcquisitionStart.send_command()
            raw_image = cam.data_stream[0].get_image()
            if raw_image is None:
                print("Getting image failed.")
                continue    
            numpy_image = raw_image.get_numpy_array()
            if numpy_image is None:
                print("The numpy image is None.")
            image_list.append(numpy_image)
            cam.AcquisitionStop.send_command()
        # cam.AcquisitionStop.send_command()
        print(len(image_list))
        img = Image.fromarray(image_list[0], 'L')
        img.show()
    else:
        print("The camer is not Color camera.")
    cam.stream_off()

def TestDevice2(device, num):
    global image_list
    for i in range(num):
        device.AcquisitionStart.send_command()
        raw_image = device.data_stream[0].get_image()
        if raw_image is None:
            print("Getting image failed.")
            continue    
        numpy_image = raw_image.get_numpy_array()
        if numpy_image is None:
            print("The" + i + "th image is None.")
        # img = Image.fromarray(numpy_image, 'L')
        # img.show()
        image_list.append(numpy_image)
        device.AcquisitionStop.send_command()
    print(len(image_list))

def TestDevice(device, num):
    global image_list
    for i in range(num):
        device.TriggerSoftware.send_command()
        raw_image = device.data_stream[0].get_image()
        if raw_image is None:
            print("Getting image failed.")
            continue    
        numpy_image = raw_image.get_numpy_array()
        if numpy_image is None:
            print("The" + i + "th image is None.")
        # img = Image.fromarray(numpy_image, 'L')
        # img.show()
        image_list.append(numpy_image)
    print(len(image_list))


def main():
    global image_list
    image_list = []
    # InitializeAndTestDevice()
    InitializeAndTestDeviceAcquisitionMode()

    # initialize_and_test_camera_thread = threading.Thread(target=InitializeAndTestDevice)
    # initialize_and_test_camera_thread_AcquisitionMode = threading.Thread(target=InitializeAndTestDeviceAcquistionMode)

    # initialize_and_test_camera_thread.start()
    # initialize_and_test_camera_thread_AcquisitionMode.start()

    # initialize_and_test_camera_thread.join()
    # initialize_and_test_camera_thread_AcquisitionMode.join()

if __name__ == "__main__":
    main()
