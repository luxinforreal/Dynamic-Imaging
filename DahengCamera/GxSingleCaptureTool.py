# version:1.0.1905.9051
import gxipy as gx
import time
import cv2

corp_height = 800
corp_width = 640


def main():
    # print the demo information
    print("")
    print("-------------------------------------------------------------")
    print("Sample to show how to acquire color image continuously and show acquired image.")
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

    # open the first device
    cam = device_manager.open_device_by_index(1)

    # exit when the camera is a mono camera
    if cam.PixelColorFilter.is_implemented() is False:
        print("This sample does not support mono camera.")
        cam.close_device()
        return

    # set continuous acquisition
    cam.TriggerMode.set(gx.GxSwitchEntry.OFF)

    # set exposure
    cam.ExposureTime.set(50000.0)

    cam.BalanceWhiteAuto.set(gx.GxAutoEntry.CONTINUOUS)

    # set gain
    cam.Gain.set(0.0)

    # get param of improving image quality
    if cam.GammaParam.is_readable():
        gamma_value = cam.GammaParam.get()
        gamma_lut = gx.Utility.get_gamma_lut(gamma_value)
    else:
        gamma_lut = None
    if cam.ContrastParam.is_readable():
        contrast_value = cam.ContrastParam.get()
        contrast_lut = gx.Utility.get_contrast_lut(contrast_value)
    else:
        contrast_lut = None
    if cam.ColorCorrectionParam.is_readable():
        color_correction_param = cam.ColorCorrectionParam.get()
    else:
        color_correction_param = 0
    max_width = cam.WidthMax.get()
    max_height = cam.HeightMax.get()
    # start data acquisition
    cam.stream_on()
    cv2.namedWindow("666", cv2.WINDOW_NORMAL)
    # acquisition image: num is the image number
    # num = 1
    # for i in range(num):
    while True:
        # get raw image
        if len(cam.data_stream) > 0:
            raw_image = cam.data_stream[0].get_image()
            if raw_image is None:
                print("Getting image failed.")
                continue

            # get RGB image from raw image
            rgb_image = raw_image.convert("RGB")
            if rgb_image is None:
                continue

            # improve image quality
            # rgb_image.image_improvement(color_correction_param, contrast_lut, gamma_lut)

            # create numpy array with data from raw image
            numpy_image = rgb_image.get_numpy_array()
            numpy_image = cv2.cvtColor(numpy_image,cv2.COLOR_BGR2RGB)
            numpy_image = cv2.flip(numpy_image,-1)
            if numpy_image is None:
                continue
            # draw_1 = cv2.rectangle(numpy_image, ((max_width-corp_width)/2, (max_height-corp_height)/2), ((max_width+corp_width)/2, (max_height+corp_height)/2), (0, 255, 0), 2)
            draw_1 = cv2.rectangle(numpy_image.copy(), (320, 112), (960, 912), (0, 255, 0), 2)
            # show acquired image
            # r = cv2.findChessboardCorners(numpy_image,(12,8))
            cv2.imshow("666", draw_1)
            # print height, width, and frame ID of the acquisition image
            key = cv2.waitKey(1) & 0xFF
            if (key == ord('s')):
                print("Frame ID: %d   Height: %d   Width: %d"
                      % (raw_image.get_frame_id(), raw_image.get_height(), raw_image.get_width()))
                corped = numpy_image[112:912,320:960]
                filename = time.strftime("%H_%M_%S", time.localtime())
                cv2.imwrite(filename+".bmp",numpy_image)
                cv2.imwrite(filename +"_corped"+ ".bmp", corped)
            if key == ord('q'):
                break

    # stop data acquisition
    cam.stream_off()

    # close device
    cam.close_device()


if __name__ == "__main__":
    main()
