'''
Description: 重写DMD进行SPI代码的实现,调用PyQt界面程序
version: 2.0
Author: luxin
Date: 2024-02-29 21:05:46
LastEditTime: 2024-03-02 14:31:42
'''
import os
import sys 
import numpy as np  
from ctypes import *
import matplotlib.pyplot as plt

import PySide2
from PySide2 import QtWidgets
from PySide2.QtCore import QDir
from PySide2.QtWidgets import QFileDialog, QTabWidget
from PySide2.QtGui import QTextCharFormat, QColor, QTextCursor

from main import qtwindow

play_mode = 1
folder_path = "D:/speckle pattern/bmp/064"
# folder_path = "D:/speckle pattern/RandomFiled1280x800/bmp/064"
save_path = "C:/Polarization experimental data/target/wave plate/angle/speckle"

# initial app instance
app = QtWidgets.QApplication(sys.argv)
b = QTabWidget()
window = qtwindow()
b.insertTab(0, window, "设备1")
b.setMinimumSize(1000, 770)
b.setWindowTitle("Python_FL_DLP_HS_Demo_Updated_LX")
b.show()
b.setCurrentIndex(0)
app.exec_()

# build command sequence - initialize
window.on_pushButton_Init_clicked()
window.on_pushButton_CMD_DeviceInfo_clicked()
window.on_pushButton_CMD_CX_clicked()
window.on_pushButton_CMD_SetParam_clicked()
window.on_pushButton_ChooseTwoPic_clicked(folder_path)
window.on_pushButton_SendTwo_clicked()

# build command sequence - execute
'''play_mode corresponding options
    type1 = 0
    if self.comboBox_CMD_Play.currentText() == "内部单次":
        type1 = 1
    elif self.comboBox_CMD_Play.currentText() == "内部循环":
        type1 = 2
    elif self.comboBox_CMD_Play.currentText() == "外部单次":
        type1 = 3
    elif self.comboBox_CMD_Play.currentText() == "外部循环":
        type1 = 4
    elif self.comboBox_CMD_Play.currentText() == "可变序列内部单次":
        type1 = 14
    elif self.comboBox_CMD_Play.currentText() == "可变序列内部循环":
        type1 = 15
    elif self.comboBox_CMD_Play.currentText() == "可变序列外部单次":
        type1 = 16
    elif self.comboBox_CMD_Play.currentText() == "可变序列外部循环":
        type1 = 17 
    # Param_StartP = int(self.lineEdit_PlayOffset.text())
    # Param_PlayPicnum = int(self.lineEdit_PicCount.text())
    Param_Mode: type1播放模式
    Param_StartP = param_startp : 起始播放位置
    Param_PlayPicnum = param_playpicnum : 截止播放位置
    Param_Rate: 采集帧率
    Param_Path: 散斑路径
'''
window.on_pushButton_CMD_Play_clicked(play_mode, 1, 1500, 20, folder_path, save_path)

# build command sequence - release source