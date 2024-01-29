'''
Descripttion: 尝试总结出硬件触发的代码实例
version: 1.0
Author: luxin
Date: 2024-01-29 10:39:23
LastEditTime: 2024-01-29 10:39:41
'''
import os
import sys
from ctypes import *

import PySide2
from PySide2 import QtWidgets
from PySide2.QtCore import QDir
from PySide2.QtGui import QTextCharFormat, QColor, QTextCursor
from PySide2.QtWidgets import QFileDialog, QTabWidget

# UDP接收线程
from UDPThread import udppthread
# UI界面
from ui_main import Ui_MainWindow