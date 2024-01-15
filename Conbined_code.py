import random
import gxipy as gx
import numpy as np
from ctypes import *
from PIL import Image
from MyThreadFunc import *

# 转台控制动态链接库
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

# 这部分设置三个转台的位置信息 返回三个轴的位置信息
# def set_zt_position0():
#         iPos0 = c_int32(0)
#         pPos0 = pointer(iPos0)
#         MT_API.MT_Get_Axis_Software_P_Now(0, pPos0)
#         print("第0轴当前的位置是=", iPos0)
#         MT_API.MT_Set_Axis_Position_P_Target_Rel(0, position0)
#         time.sleep(1)
#         MT_API.MT_Get_Axis_Software_P_Now(0, pPos0)
#         print("第0轴移动后的位置是=", iPos0)


# def set_zt_position1():
#         iPos1 = c_int32(0)
#         pPos1 = pointer(iPos1)
#         MT_API.MT_Get_Axis_Software_P_Now(1, pPos1)
#         print("第1轴当前的位置是=", iPos1)
#         MT_API.MT_Set_Axis_Position_P_Target_Rel(1, position1)
#         time.sleep(1)
#         MT_API.MT_Get_Axis_Software_P_Now(1, pPos1)
#         print("第1轴移动后的位置是=", iPos1)

# def set_zt_position2():
#         iPos2 = c_int32(0)
#         pPos2 = pointer(iPos2)
#         MT_API.MT_Get_Axis_Software_P_Now(2, pPos2)
#         print("第2轴当前的位置是=", iPos2)
#         MT_API.MT_Set_Axis_Position_P_Target_Rel(2, position2)
#         time.sleep(1)
#         MT_API.MT_Get_Axis_Software_P_Now(2, pPos2)
#         print("第2轴移动后的位置是=", iPos2)


# 实现feedback的移动的函数功能
'''
    1.error_x error_y 分别代表的是亮度图像中心和市场中心之间的差值,利用PID算法实现转台控制
    2.相机的像素为2048x2448,相机中心像素为[1024, 1224]
'''
# obj_cam_operation = ...
# def fun():
#     global openclose
#     global error_x
#     global error_y
#     while (1):
#         error_x = float(obj_cam_operation.cx) - 160
#         error_y = 128 - float(obj_cam_operation.cy)
#
#         if openclose == 1:
#             control_x = int(100 * error_x)
#             control_y = int(100 * error_y)
#
#             MT_API.MT_Set_Axis_Position_P_Target_Rel(2, control_x)
#             MT_API.MT_Set_Axis_Position_P_Target_Rel(1, control_y)
#
#         if openclose == 0:
#             continue
#
#         # if position1>=10000 or position1<=-10000 or position2>=10000 or position2<=-10000:
#         #     break

# --------------------------转台 & 相机控制代码-------------------------
"""
代码中涉及的函数功能如下：

- 图像存储函数：
    1. transfer_and_save_image(): 处理的是给定image_list三维数组从中存储图片
    2. transfer_and_save_image2(): 处理的是单独在循环当中处理numpy_array存储为.png格式

- 图像获取函数：
    1. acq_color(): 提供的彩色图片获取接口
    2. acq_mono():  提供的黑白图像获取接口
    3. acq_mono1(): 控制转台校准物体位置到中心
    3. acq_mono2(): 控制转台获取光强度值函数(mian)
    
- 转台控制函数：
    1. func(): PID转台控制程序模板
    2. func2(): index=0, 2 轴控制
    3. func3(): index=0, 1 轴控制
    4. func4(): 添加确定导引灯中心位置控制代码
    
    
- 图像处理函数：
    1. erased_led(): 消除图像中led导引灯的干扰 // 其他方法？
    2. acquire_block(): 裁剪获取的图像为随机散斑大小图像
    3. image_processing(): 图像总处理函数, 获取光强序列
"""

# image processing
def image_processing(image_list):
    intensity = []                       # 最后传输到DGI完成物理方法成像的变量
    print(len(image_list))
    for i in range(len(image_list)):
        acquire_block(image_list[i], 800, 1280, i)
    for i in range(len(image_list)):
        sum = np.sum(image_list[i])
        intensity.append(sum)
    # 测试传输的变量正确性，最后版本删除这部分的代码
    print(image_list)
    print(image_list[0])
    print(image_list[0].shape)
    print(intensity)
    # normalization intensity
    # max_value = max(intensity)
    # min_value = min(intensity)
    # print(max_value, min_value)
    # for i in range(len(intensity)):
    #     intensity[i] = (intensity[i] - min_value) / (max_value - min_value)
    # print(intensity)
    return intensity


# slices the picture
def acquire_block(numpy_image, a, b, i):
    new_image = []
    center = [1223, 1023]
    print("The Width of the Image is:%d  The Height of the Image is:%d"
          % (len(numpy_image[:, 1]), len(numpy_image[0])))
    sx = int(center[0] - a / 2)
    sy = int(center[1] - b / 2)
    # check the position 这里print的信息最后都可以慢慢删除，测试代码输出是否正确
    # print("The start position x:%d The start position y:%d" % (sx, sy))
    new_image = numpy_image[sx:sx + a, sy: sy + b]
    print("The Width of the new Image is:%d  The Height of the nwe Image is:%d"
          % (len(new_image[:, 1]), len(new_image[0])))
    # print(new_image)
    xy = np.where(new_image >= 255)
    new_image[xy] = 0

def transfer_and_save_image(image_list):
    # print(Image_list)
    for i in range(len(image_list)):
        img = Image.fromarray(image_list[i], 'L')
        filename = "image_%d.png" % (i + 1)
        img.save(filename, "jpeg")
        # img.show()

def transfer_and_save_image2(numpy_image, i):
    numpy_image = Image.fromarray(numpy_image, 'L')
    filename = "image_%d.png" % (i + 1)
    numpy_image.save(filename, 'png')

# acquire color images
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


# control function template
def func(x, y, center, i, num):
    global error_x
    global error_y
    print("Tracing............")
    print(x, y)
    error_x = int(x) - center[0]
    error_y = center[1] - int(y)
    if i <= num:
        control_x = int(100 * error_x)
        control_y = int(100 * error_y)

        # MT_API.MT_Set_Axis_Position_P_Target_Rel(2, control_x)
        # MT_API.MT_Set_Axis_Position_P_Target_Rel(1, control_y)
    else:
        return


# control axis 1, 2
def func2(x, y, center):
    global error_x
    global error_y
    print("Tracing............")
    if x is not None and y is not None:
        print("Object x axis : %d  Object y axis : %d  "
              % (x, y))
        error_x = float(x) - center[0]
        error_y = center[1] - float(y)
        control_x = int(100 * error_x)
        control_y = int(100 * error_y)
        print("Error x : %d  Error y : %d  " % (error_x, error_y))
    print("Control x : %d  Control y : %d  "
          % (control_x, control_y))
    # MT_API.MT_Set_Axis_Position_P_Target_Rel(2, control_x)
    # MT_API.MT_Set_Axis_Position_P_Target_Rel(1, control_y)


# control axis 0, 1
def func3(x, y, center):
    global error_x
    global error_y
    print("Tracing............")
    print(center)
    # if x.isnan() is False and y .isnan() is False:
    if str(x) != 'nan' and str(y) != 'nan':
        # print("Object x axis : %d  Object y axis : %d  "
        #       % (x, y))
        error_x = float(x) - center[0]
        error_y = center[1] - float(y)
        control_x = int(50 * error_x)
        control_y = int(50 * error_y)
        print("Error x : %d  Error y : %d  "
              % (error_x, error_y))
        print("Control x : %d  Control y : %d  "
              % (control_x, control_y))
        # MT_API.MT_Set_Axis_Position_P_Target_Rel(0, control_x)
        # MT_API.MT_Set_Axis_Position_P_Target_Rel(1, control_y)
    else:
        return

# conditional added
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
        if error_x <= 20 and error_y <= 20:
            control_x = 0
            control_y = 0
        else:
            control_x = control_x
            control_y = control_y
        # print("Error x : %d  Error y : %d  " % (error_x, error_y))
        # print("Control x : %d  Control y : %d " % (control_x, control_y))
        MT_API.MT_Set_Axis_Position_P_Target_Rel(0, control_x)
        MT_API.MT_Set_Axis_Position_P_Target_Rel(1, control_y)
    else:
        return

def acq_mono(device, num):
    for i in range(num):
        time.sleep(0.1)

        device.TriggerSoftware.send_command()

        raw_image = device.data_stream[0].get_image()
        if raw_image is None:
            print("Getting image failed.")
            continue
        numpy_image = raw_image.get_numpy_array()
        if numpy_image is None:
            continue
        img = Image.fromarray(numpy_image, 'L')
        img.show()
        print("Frame ID: %d   Height: %d   Width: %d"
              % (raw_image.get_frame_id(), raw_image.get_height(), raw_image.get_width()))


def acq_mono2(device, num):
    """
        捕获图像的时候每次计算intensity中心和图像中心之间的距离
    """
    global cx
    global cy
    image_list = []
    center = np.array([1223, 1023])
    for i in range(num):
        time.sleep(0.05)
        device.TriggerSoftware.send_command()

        raw_image = device.data_stream[0].get_image()
        if raw_image is None:
            print("Getting image failed.")
            continue
        numpy_image = raw_image.get_numpy_array()
        cxy = np.where(numpy_image >= 255)
        if len(cxy) != 0:
            print("Round:", i)
            print("Center of the object:", cxy)
            cx = np.mean(cxy[1])
            cy = np.mean(cxy[0])
            print("Numpy image: \n", numpy_image)
            func3(cx, cy, center)
            image_list.append(numpy_image)
        else:
            continue
        if numpy_image is None:
            continue
    print("--------------------transfer and save image------------------")
    print("Image number:", len(image_list))
    image_processing(image_list)
    # transfer_and_save_image(image_list)
    return image_list



def TriggerFunction():
    # print the demo information
    print("")
    print("---------Acquire mono or color image by soft trigger---------")
    print("")
    print("Initializing......")
    print("")

    # create a device manager
    device_manager = gx.DeviceManager()
    dev_num, dev_info_list = device_manager.update_device_list()
    if dev_num is 0:
        print("Number of enumerated devices is 0")
        return
    cam = device_manager.open_device_by_index(1)
    cam.ExposureTime.set(10000)
    cam.Gain.set(10.0)

    if dev_info_list[0].get("device_class") == gx.GxDeviceClassList.USB2:
        cam.TriggerMode.set(gx.GxSwitchEntry.ON)
    else:
        cam.TriggerMode.set(gx.GxSwitchEntry.ON)
        cam.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)

    cam.stream_on()
    if cam.PixelColorFilter.is_implemented() is True:
        acq_color(cam, 50)
    else:
        acq_mono2(cam, 50)

    cam.stream_off()
    cam.close_device()




if __name__ == "__main__":
    global cx
    global cy
    global error_x
    global error_y
    open_zt()
    set_zt_initial()
    TriggerFunction()
    close_zt()

