'''
Descripttion: 重写DMD进行SPI代码的实现,调用PyQt
version: 1.0
Author: luxin
Date: 2024-02-29 21:05:46
LastEditTime: 2024-02-29 21:49:29
'''
import os
import sys 
import numpy as np  
from ctypes import *
import matplotlib.pyplot as plt

import PySide2
from PySide2 import QtWidgets
from PySide2.QtCore import QDir
from PySide2.QtGui import QTextCharFormat, QColor, QTextCursor
from PySide2.QtWidgets import QFileDialog, QTabWidget

from UDPThread import udppthread
from ui_main import Ui_MainWindow
from main import qtwindow

folder_path = "D:/speckle pattern/bmp/070"

app = QtWidgets.QApplication(sys.argv)
window = qtwindow()
window.show()

window.on_pushButton_Init_clicked()
window.on_pushButton_CMD_DeviceInfo_clicked()
window.on_pushButton_CMD_SetParam_clicked()
window.on_pushButton_ChooseTwoPic_clicked(folder_path)
# 给出文件夹内的图片数量，发送图片樟树和起始加载位置的设置



app.exec_()

# def load_bmp_from_directory(self, directory_path):
#     # 接收预设的文件夹路径
#     dir1 = QDir(directory_path)
    
#     # 设置过滤器，只包含.bmp文件
#     filter1 = ['*.bmp']

#     # 获取目录下所有满足条件的文件条目信息
#     fileInfo = dir1.entryInfoList(filter1, QDir.Files | QDir.Readable, QDir.Name)

#     # 初始化一个列表来存储加载的图片数据
#     bmp_images = []

#     # 遍历文件信息，加载每个.bmp文件
#     for info in fileInfo:
#         # 获取绝对文件路径
#         abs_file_path = info.absoluteFilePath()
        
#         # 加载.bmp图片
#         try:
#             img = cv2.imread(abs_file_path, cv2.IMREAD_GRAYSCALE)
#             if img is not None:
#                 bmp_images.append(img)
#         except Exception as e:
#             print(f"无法加载图片文件: {abs_file_path}, 错误原因: {e}")

#     # 对加载成功的图片进行进一步处理...
#     # （此处省略，根据你的需求进行图片处理或显示等操作）

#     # 显示bmp图片数量（如果需要）
#     num_of_bmps = len(bmp_images)
#     self.lineEdit_Picnum_Dir.setText(str(num_of_bmps))

# # 使用示例
# predefined_directory = "C:/Your_predefined_directory"
# self.load_bmp_from_directory(predefined_directory)
