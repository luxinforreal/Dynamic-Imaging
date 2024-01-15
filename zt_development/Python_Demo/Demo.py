from ctypes import *
import time

# 64位系统和32位系统的dll 不一样，注意切换
MT_API = windll.LoadLibrary("MT_API.dll")

#  https://docs.python.org/3.6/library/ctypes.html 使用说明

# 设置函数的参数类型，需要使用的函数请参照二次开发手册设置
# Python默认返回int，非int需要指定返回值
# Python 默认参数为int值，非int值需要指定参数类型
# int = int32

MT_API.MT_Open_UART.argtypes = [c_char_p]
##############################################
# 所有的接口函数的单位为  脉冲数，不是物理单位 ，有一个固定比例的关系，和机械参数有关系
# 有MT_Help打头的函数可以辅助计算，也可以人工计算换算
# 例如2mm螺距导程的直线台，32细分的情况，32*200脉冲(电机转1圈)=2mm  1mm=3200个脉冲
##############################################


# 初始化函数，必须且只能执行一次，特别注意，和DeInit配对使用，未执行
# MT_Init前，其他函数的行为都是错误和不可预测的
MT_API.MT_Init()

# 如何进行物理单位和脉冲单位的转换示例,Python默认是整形，其它类型使用前要定义
# 直线台19200脉冲转物理量,细分32，直线传动比1，螺距2mm
MT_API.MT_Help_Step_Line_Steps_To_Real.argtypes = [c_double, c_int32, c_double, c_double, c_int32]
MT_API.MT_Help_Step_Line_Steps_To_Real.restype=c_double
fReal = MT_API.MT_Help_Step_Line_Steps_To_Real(1.8, 32, 2, 1, 19200)

# 旋转台6400脉冲转物理量,细分32，传动比180
MT_API.MT_Help_Step_Circle_Steps_To_Real.argtypes = [c_double, c_int32, c_double, c_int32]
MT_API.MT_Help_Step_Circle_Steps_To_Real.restype=c_double
fReal = MT_API.MT_Help_Step_Circle_Steps_To_Real(1.8, 32, 180, 6400)

# 直线台2mm物理量转脉冲,细分32，直线传动比1，螺距2mm
MT_API.MT_Help_Step_Line_Real_To_Steps.argtypes = [c_double, c_int32, c_double, c_double, c_double]
MT_API.MT_Help_Step_Line_Real_To_Steps.restype=c_int32
iSteps = MT_API.MT_Help_Step_Line_Real_To_Steps(1.8, 32, 2, 1, 2)

# 旋转台360°物理量转脉冲,细分32，旋转传动比180
MT_API.MT_Help_Step_Circle_Real_To_Steps.argtypes = [c_double, c_int32, c_double, c_double]
MT_API.MT_Help_Step_Circle_Real_To_Steps.restype=c_int32
iSteps = MT_API.MT_Help_Step_Circle_Real_To_Steps(1.8, 32, 180, 360)



# 使用USB接口，或者使用串口，或者使用网口
# MT_API.MT_Open_USB()

# MT_API.MT_Open_Net(192,168,0,168,8888)

# 根据实际情况，修改串口号  python好像不支持char*，先转换为byte*

# MT_API.MT_Open_UART_Unicode("COM7")
charPointer=bytes("COM3", "gbk")
# MT_API.MT_Open_UART("COM7")
MT_API.MT_Open_UART(charPointer)

iR = MT_API.MT_Check()
# iR =0 为成功
print("iR=", iR)


# 停止指定正在运行的电机，序号从0开始,对应第一轴
# MT_API.MT_Set_Axis_Halt(0)
# 停止所有正在运行的电机
MT_API.MT_Set_Axis_Halt_All()

# 读取当前的位置,传入电机序号和一个整数指针
iPos = c_int32(0)
pPos = pointer(iPos)

MT_API.MT_Get_Axis_Software_P_Now(0, pPos)

print("iPos=", iPos)
# 设置当前位置为0点 ,也可以设置为任意坐标值，后续坐标对应变化
MT_API.MT_Set_Axis_Software_P(0, 0)

# example 1
# 第一轴归零，碰到零位或者限位停止，或者5S后停止，
# 进入归零模式，上电后所有电机默认为位置模式
MT_API.MT_Set_Axis_Mode_Home(0)
MT_API.MT_Set_Axis_Home_Acc(0, 2000)
MT_API.MT_Set_Axis_Home_Dec(0, 2000)

# 一般都是负向归零，碰到负限位或者零位停止，没有零位的情况下，负限位为零位
# 整个坐标系保持在正值范围内
MT_API.MT_Set_Axis_Home_V(0, -2000)

time.sleep(5)

# 如果已经找到，当前位置自动修改为0，此函数无效，如果没找到，则强制停止，当前位置坐标不变
# 可以通过后面使用的读取状态函数来实现判断是否完成
MT_API.MT_Set_Axis_Home_Stop(0)

# example 2
# 切换到位置模式 加速度 减速度 最大速度（匀速运行速度）
MT_API.MT_Set_Axis_Mode_Position(1)
MT_API.MT_Set_Axis_Position_Acc(1, 3000)
MT_API.MT_Set_Axis_Position_Dec(1, 3000)

MT_API.MT_Set_Axis_Position_V_Max(1, 5000)


# 状态变量
iRun = c_int32(0)

pRun = pointer(iRun)


# 相对移动模式，偏移量，可正可负

MT_API.MT_Get_Axis_Software_P_Now(1, pPos)
print("相对移动前位置=", iPos)

MT_API.MT_Set_Axis_Position_P_Target_Rel(1, 5000)

time.sleep(0.5)
# 读取当前运动状态
MT_API.MT_Get_Axis_Status_Run(1, pRun)

print("iRun=", iRun)

time.sleep(2)

MT_API.MT_Get_Axis_Status_Run(1, pRun)

print("iRun=", iRun)

# 停止后的坐标位置
MT_API.MT_Get_Axis_Software_P_Now(1, pPos)
print("相对移动5000后位置=", iPos)

MT_API.MT_Set_Axis_Position_P_Target_Rel(1, -2000)

time.sleep(0.5)

MT_API.MT_Get_Axis_Status_Run(1, pRun)

print("iRun=", iRun)

time.sleep(2)

MT_API.MT_Get_Axis_Status_Run(1, pRun)

print("iRun=", iRun)

MT_API.MT_Get_Axis_Software_P_Now(1, pPos)
print("相对移动-2000后位置=", iPos)

# 向坐标原点运行,绝对方式，直接指定坐标位置
MT_API.MT_Set_Axis_Position_P_Target_Abs(1, 0)

time.sleep(1)

# 改变主意了，不想到原点，实时修改目标位置，电机自动进行方向判断
MT_API.MT_Set_Axis_Position_P_Target_Abs(1, 10000)

time.sleep(1)

# 停止，不运行了

MT_API.MT_Set_Axis_Position_Stop(1)

MT_API.MT_Get_Axis_Software_P_Now(1, pPos)
print("iPos=", iPos)
# 关闭通信口
MT_API.MT_Close_UART()
MT_API.MT_Close_Net()
MT_API.MT_Close_USB()
# DeInit最后调用，释放资源
MT_API.MT_DeInit()