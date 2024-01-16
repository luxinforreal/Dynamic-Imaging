# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 770)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_28 = QGridLayout(self.centralwidget)
        self.gridLayout_28.setObjectName(u"gridLayout_28")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.lineEdit_XWJ_Port = QLineEdit(self.groupBox)
        self.lineEdit_XWJ_Port.setObjectName(u"lineEdit_XWJ_Port")

        self.gridLayout_2.addWidget(self.lineEdit_XWJ_Port, 2, 3, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 1, 2, 1, 1)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 2)

        self.pushButton_Init = QPushButton(self.groupBox)
        self.pushButton_Init.setObjectName(u"pushButton_Init")

        self.gridLayout_2.addWidget(self.pushButton_Init, 3, 0, 1, 4)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)

        self.lineEdit_XWJ_IP = QLineEdit(self.groupBox)
        self.lineEdit_XWJ_IP.setObjectName(u"lineEdit_XWJ_IP")

        self.gridLayout_2.addWidget(self.lineEdit_XWJ_IP, 2, 1, 1, 1)

        self.lineEdit_ZJ_Port = QLineEdit(self.groupBox)
        self.lineEdit_ZJ_Port.setObjectName(u"lineEdit_ZJ_Port")

        self.gridLayout_2.addWidget(self.lineEdit_ZJ_Port, 1, 3, 1, 1)

        self.pushButton_CMD_CX = QPushButton(self.groupBox)
        self.pushButton_CMD_CX.setObjectName(u"pushButton_CMD_CX")

        self.gridLayout_2.addWidget(self.pushButton_CMD_CX, 4, 0, 1, 4)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)

        self.pushButton_CMD_DeviceInfo = QPushButton(self.groupBox)
        self.pushButton_CMD_DeviceInfo.setObjectName(u"pushButton_CMD_DeviceInfo")

        self.gridLayout_2.addWidget(self.pushButton_CMD_DeviceInfo, 5, 0, 1, 4)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 2, 2, 1, 1)

        self.lineEdit_ZJ_IP = QLineEdit(self.groupBox)
        self.lineEdit_ZJ_IP.setObjectName(u"lineEdit_ZJ_IP")

        self.gridLayout_2.addWidget(self.lineEdit_ZJ_IP, 1, 1, 1, 1)

        self.comboBox_DeviceID = QComboBox(self.groupBox)
        self.comboBox_DeviceID.addItem("")
        self.comboBox_DeviceID.addItem("")
        self.comboBox_DeviceID.addItem("")
        self.comboBox_DeviceID.addItem("")
        self.comboBox_DeviceID.addItem("")
        self.comboBox_DeviceID.addItem("")
        self.comboBox_DeviceID.addItem("")
        self.comboBox_DeviceID.addItem("")
        self.comboBox_DeviceID.addItem("")
        self.comboBox_DeviceID.addItem("")
        self.comboBox_DeviceID.setObjectName(u"comboBox_DeviceID")

        self.gridLayout_2.addWidget(self.comboBox_DeviceID, 0, 2, 1, 2)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 6, 0, 1, 1)

        self.textEdit_DeviceInfo = QTextEdit(self.groupBox)
        self.textEdit_DeviceInfo.setObjectName(u"textEdit_DeviceInfo")
        font = QFont()
        font.setPointSize(9)
        self.textEdit_DeviceInfo.setFont(font)
        self.textEdit_DeviceInfo.setReadOnly(True)

        self.gridLayout_2.addWidget(self.textEdit_DeviceInfo, 6, 1, 1, 3)


        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)


        self.gridLayout_28.addLayout(self.gridLayout, 0, 0, 3, 1)

        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_12 = QGridLayout(self.groupBox_4)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_11 = QGridLayout()
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.lineEdit_Param_CFDelay = QLineEdit(self.groupBox_4)
        self.lineEdit_Param_CFDelay.setObjectName(u"lineEdit_Param_CFDelay")

        self.gridLayout_11.addWidget(self.lineEdit_Param_CFDelay, 5, 1, 1, 2)

        self.label_11 = QLabel(self.groupBox_4)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_11.addWidget(self.label_11, 4, 0, 1, 1)

        self.checkBox_Param_SC_DOWM = QCheckBox(self.groupBox_4)
        self.buttonGroup_2 = QButtonGroup(MainWindow)
        self.buttonGroup_2.setObjectName(u"buttonGroup_2")
        self.buttonGroup_2.addButton(self.checkBox_Param_SC_DOWM)
        self.checkBox_Param_SC_DOWM.setObjectName(u"checkBox_Param_SC_DOWM")

        self.gridLayout_11.addWidget(self.checkBox_Param_SC_DOWM, 2, 2, 1, 1)

        self.checkBox_Param_SR_UP = QCheckBox(self.groupBox_4)
        self.buttonGroup = QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.checkBox_Param_SR_UP)
        self.checkBox_Param_SR_UP.setObjectName(u"checkBox_Param_SR_UP")
        self.checkBox_Param_SR_UP.setChecked(True)

        self.gridLayout_11.addWidget(self.checkBox_Param_SR_UP, 1, 1, 1, 1)

        self.label_9 = QLabel(self.groupBox_4)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_11.addWidget(self.label_9, 2, 0, 1, 1)

        self.label_10 = QLabel(self.groupBox_4)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_11.addWidget(self.label_10, 3, 0, 1, 1)

        self.checkBox_Param_SC_UP = QCheckBox(self.groupBox_4)
        self.buttonGroup_2.addButton(self.checkBox_Param_SC_UP)
        self.checkBox_Param_SC_UP.setObjectName(u"checkBox_Param_SC_UP")
        self.checkBox_Param_SC_UP.setChecked(True)

        self.gridLayout_11.addWidget(self.checkBox_Param_SC_UP, 2, 1, 1, 1)

        self.lineEdit_Param_CFPicnum = QLineEdit(self.groupBox_4)
        self.lineEdit_Param_CFPicnum.setObjectName(u"lineEdit_Param_CFPicnum")

        self.gridLayout_11.addWidget(self.lineEdit_Param_CFPicnum, 4, 1, 1, 2)

        self.label_8 = QLabel(self.groupBox_4)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_11.addWidget(self.label_8, 1, 0, 1, 1)

        self.lineEdit_Param_Gray = QLineEdit(self.groupBox_4)
        self.lineEdit_Param_Gray.setObjectName(u"lineEdit_Param_Gray")

        self.gridLayout_11.addWidget(self.lineEdit_Param_Gray, 3, 1, 1, 2)

        self.lineEdit_Param_Delay = QLineEdit(self.groupBox_4)
        self.lineEdit_Param_Delay.setObjectName(u"lineEdit_Param_Delay")

        self.gridLayout_11.addWidget(self.lineEdit_Param_Delay, 0, 1, 1, 2)

        self.label_7 = QLabel(self.groupBox_4)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_11.addWidget(self.label_7, 0, 0, 1, 1)

        self.label_12 = QLabel(self.groupBox_4)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_11.addWidget(self.label_12, 5, 0, 1, 1)

        self.checkBox_Param_SR_DOWM = QCheckBox(self.groupBox_4)
        self.buttonGroup.addButton(self.checkBox_Param_SR_DOWM)
        self.checkBox_Param_SR_DOWM.setObjectName(u"checkBox_Param_SR_DOWM")

        self.gridLayout_11.addWidget(self.checkBox_Param_SR_DOWM, 1, 2, 1, 1)

        self.pushButton_CMD_SetParam = QPushButton(self.groupBox_4)
        self.pushButton_CMD_SetParam.setObjectName(u"pushButton_CMD_SetParam")

        self.gridLayout_11.addWidget(self.pushButton_CMD_SetParam, 6, 0, 1, 3)


        self.gridLayout_12.addLayout(self.gridLayout_11, 0, 0, 1, 1)


        self.gridLayout_10.addWidget(self.groupBox_4, 0, 0, 1, 1)


        self.gridLayout_28.addLayout(self.gridLayout_10, 0, 1, 1, 1)

        self.gridLayout_13 = QGridLayout()
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.groupBox_5 = QGroupBox(self.centralwidget)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.gridLayout_14 = QGridLayout(self.groupBox_5)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_15 = QGridLayout()
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.pushButton_ChooseBin = QPushButton(self.groupBox_5)
        self.pushButton_ChooseBin.setObjectName(u"pushButton_ChooseBin")

        self.gridLayout_15.addWidget(self.pushButton_ChooseBin, 0, 2, 1, 1)

        self.pushButton_SendTwo = QPushButton(self.groupBox_5)
        self.pushButton_SendTwo.setObjectName(u"pushButton_SendTwo")

        self.gridLayout_15.addWidget(self.pushButton_SendTwo, 4, 0, 1, 1)

        self.lineEdit_SendPicnum = QLineEdit(self.groupBox_5)
        self.lineEdit_SendPicnum.setObjectName(u"lineEdit_SendPicnum")

        self.gridLayout_15.addWidget(self.lineEdit_SendPicnum, 2, 1, 1, 2)

        self.label_13 = QLabel(self.groupBox_5)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_15.addWidget(self.label_13, 3, 0, 1, 1)

        self.lineEdit_SendPicStarP = QLineEdit(self.groupBox_5)
        self.lineEdit_SendPicStarP.setObjectName(u"lineEdit_SendPicStarP")

        self.gridLayout_15.addWidget(self.lineEdit_SendPicStarP, 3, 1, 1, 2)

        self.pushButton_SendEight = QPushButton(self.groupBox_5)
        self.pushButton_SendEight.setObjectName(u"pushButton_SendEight")

        self.gridLayout_15.addWidget(self.pushButton_SendEight, 4, 1, 1, 1)

        self.label_14 = QLabel(self.groupBox_5)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_15.addWidget(self.label_14, 1, 0, 1, 1)

        self.lineEdit_Picnum_Dir = QLineEdit(self.groupBox_5)
        self.lineEdit_Picnum_Dir.setObjectName(u"lineEdit_Picnum_Dir")
        self.lineEdit_Picnum_Dir.setReadOnly(True)

        self.gridLayout_15.addWidget(self.lineEdit_Picnum_Dir, 1, 1, 1, 2)

        self.pushButton_ChooseEightPic = QPushButton(self.groupBox_5)
        self.pushButton_ChooseEightPic.setObjectName(u"pushButton_ChooseEightPic")

        self.gridLayout_15.addWidget(self.pushButton_ChooseEightPic, 0, 1, 1, 1)

        self.pushButton_ChooseTwoPic = QPushButton(self.groupBox_5)
        self.pushButton_ChooseTwoPic.setObjectName(u"pushButton_ChooseTwoPic")

        self.gridLayout_15.addWidget(self.pushButton_ChooseTwoPic, 0, 0, 1, 1)

        self.label_15 = QLabel(self.groupBox_5)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_15.addWidget(self.label_15, 2, 0, 1, 1)

        self.label_16 = QLabel(self.groupBox_5)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_15.addWidget(self.label_16, 6, 0, 1, 1)

        self.pushButton_SendBin = QPushButton(self.groupBox_5)
        self.pushButton_SendBin.setObjectName(u"pushButton_SendBin")

        self.gridLayout_15.addWidget(self.pushButton_SendBin, 4, 2, 1, 1)

        self.pushButton_SendChar = QPushButton(self.groupBox_5)
        self.pushButton_SendChar.setObjectName(u"pushButton_SendChar")

        self.gridLayout_15.addWidget(self.pushButton_SendChar, 6, 1, 1, 2)

        self.label_18 = QLabel(self.groupBox_5)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_15.addWidget(self.label_18, 5, 0, 1, 1)

        self.lineEdit_Width = QLineEdit(self.groupBox_5)
        self.lineEdit_Width.setObjectName(u"lineEdit_Width")

        self.gridLayout_15.addWidget(self.lineEdit_Width, 5, 1, 1, 1)

        self.lineEdit_Height = QLineEdit(self.groupBox_5)
        self.lineEdit_Height.setObjectName(u"lineEdit_Height")

        self.gridLayout_15.addWidget(self.lineEdit_Height, 5, 2, 1, 1)


        self.gridLayout_14.addLayout(self.gridLayout_15, 0, 0, 1, 1)


        self.gridLayout_13.addWidget(self.groupBox_5, 0, 0, 1, 1)


        self.gridLayout_28.addLayout(self.gridLayout_13, 0, 2, 1, 2)

        self.gridLayout_19 = QGridLayout()
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.groupBox_7 = QGroupBox(self.centralwidget)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.gridLayout_26 = QGridLayout(self.groupBox_7)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.gridLayout_20 = QGridLayout()
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.comboBox_CMD_Play = QComboBox(self.groupBox_7)
        self.comboBox_CMD_Play.addItem("")
        self.comboBox_CMD_Play.addItem("")
        self.comboBox_CMD_Play.addItem("")
        self.comboBox_CMD_Play.addItem("")
        self.comboBox_CMD_Play.addItem("")
        self.comboBox_CMD_Play.addItem("")
        self.comboBox_CMD_Play.addItem("")
        self.comboBox_CMD_Play.addItem("")
        self.comboBox_CMD_Play.setObjectName(u"comboBox_CMD_Play")

        self.gridLayout_20.addWidget(self.comboBox_CMD_Play, 1, 0, 1, 2)

        self.label_19 = QLabel(self.groupBox_7)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_20.addWidget(self.label_19, 3, 0, 1, 1)

        self.label_17 = QLabel(self.groupBox_7)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_20.addWidget(self.label_17, 2, 0, 1, 1)

        self.lineEdit_PlayOffset = QLineEdit(self.groupBox_7)
        self.lineEdit_PlayOffset.setObjectName(u"lineEdit_PlayOffset")

        self.gridLayout_20.addWidget(self.lineEdit_PlayOffset, 2, 1, 1, 1)

        self.lineEdit_PicCount = QLineEdit(self.groupBox_7)
        self.lineEdit_PicCount.setObjectName(u"lineEdit_PicCount")

        self.gridLayout_20.addWidget(self.lineEdit_PicCount, 3, 1, 1, 1)

        self.pushButton_CMD_PlayStop = QPushButton(self.groupBox_7)
        self.pushButton_CMD_PlayStop.setObjectName(u"pushButton_CMD_PlayStop")

        self.gridLayout_20.addWidget(self.pushButton_CMD_PlayStop, 5, 0, 1, 1)

        self.pushButton_CMD_Stop = QPushButton(self.groupBox_7)
        self.pushButton_CMD_Stop.setObjectName(u"pushButton_CMD_Stop")

        self.gridLayout_20.addWidget(self.pushButton_CMD_Stop, 5, 1, 1, 1)

        self.pushButton_CMD_Play = QPushButton(self.groupBox_7)
        self.pushButton_CMD_Play.setObjectName(u"pushButton_CMD_Play")

        self.gridLayout_20.addWidget(self.pushButton_CMD_Play, 4, 0, 1, 2)


        self.gridLayout_26.addLayout(self.gridLayout_20, 0, 0, 1, 1)


        self.gridLayout_19.addWidget(self.groupBox_7, 0, 0, 1, 1)


        self.gridLayout_28.addLayout(self.gridLayout_19, 1, 1, 2, 1)

        self.gridLayout_21 = QGridLayout()
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.groupBox_8 = QGroupBox(self.centralwidget)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.gridLayout_23 = QGridLayout(self.groupBox_8)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.gridLayout_22 = QGridLayout()
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.pushButton_CMD_UPDOWM = QPushButton(self.groupBox_8)
        self.pushButton_CMD_UPDOWM.setObjectName(u"pushButton_CMD_UPDOWM")

        self.gridLayout_22.addWidget(self.pushButton_CMD_UPDOWM, 0, 0, 1, 1)

        self.pushButton_CMD_DateReverse = QPushButton(self.groupBox_8)
        self.pushButton_CMD_DateReverse.setObjectName(u"pushButton_CMD_DateReverse")

        self.gridLayout_22.addWidget(self.pushButton_CMD_DateReverse, 0, 1, 1, 1)

        self.pushButton_CMD_SoftCF = QPushButton(self.groupBox_8)
        self.pushButton_CMD_SoftCF.setObjectName(u"pushButton_CMD_SoftCF")

        self.gridLayout_22.addWidget(self.pushButton_CMD_SoftCF, 0, 2, 1, 1)

        self.pushButton_CMD_DMDFloat = QPushButton(self.groupBox_8)
        self.pushButton_CMD_DMDFloat.setObjectName(u"pushButton_CMD_DMDFloat")

        self.gridLayout_22.addWidget(self.pushButton_CMD_DMDFloat, 1, 0, 1, 1)

        self.pushButton_CMD_Reset = QPushButton(self.groupBox_8)
        self.pushButton_CMD_Reset.setObjectName(u"pushButton_CMD_Reset")

        self.gridLayout_22.addWidget(self.pushButton_CMD_Reset, 1, 2, 1, 1)


        self.gridLayout_23.addLayout(self.gridLayout_22, 0, 0, 1, 1)


        self.gridLayout_21.addWidget(self.groupBox_8, 0, 0, 1, 1)


        self.gridLayout_28.addLayout(self.gridLayout_21, 1, 2, 1, 2)

        self.gridLayout_24 = QGridLayout()
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.groupBox_9 = QGroupBox(self.centralwidget)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.gridLayout_27 = QGridLayout(self.groupBox_9)
        self.gridLayout_27.setObjectName(u"gridLayout_27")
        self.gridLayout_25 = QGridLayout()
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.textEdit_ZDY = QTextEdit(self.groupBox_9)
        self.textEdit_ZDY.setObjectName(u"textEdit_ZDY")

        self.gridLayout_25.addWidget(self.textEdit_ZDY, 0, 0, 1, 1)

        self.pushButton_SendZDYCmd = QPushButton(self.groupBox_9)
        self.pushButton_SendZDYCmd.setObjectName(u"pushButton_SendZDYCmd")

        self.gridLayout_25.addWidget(self.pushButton_SendZDYCmd, 1, 0, 1, 1)


        self.gridLayout_27.addLayout(self.gridLayout_25, 0, 0, 1, 1)


        self.gridLayout_24.addWidget(self.groupBox_9, 0, 0, 1, 1)


        self.gridLayout_28.addLayout(self.gridLayout_24, 2, 3, 2, 1)

        self.gridLayout_16 = QGridLayout()
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.groupBox_6 = QGroupBox(self.centralwidget)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.gridLayout_18 = QGridLayout(self.groupBox_6)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_17 = QGridLayout()
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.tableWidget = QTableWidget(self.groupBox_6)
        self.tableWidget.setObjectName(u"tableWidget")

        self.gridLayout_17.addWidget(self.tableWidget, 0, 0, 1, 1)

        self.pushButton_CMD_SetSequence = QPushButton(self.groupBox_6)
        self.pushButton_CMD_SetSequence.setObjectName(u"pushButton_CMD_SetSequence")

        self.gridLayout_17.addWidget(self.pushButton_CMD_SetSequence, 1, 0, 1, 1)


        self.gridLayout_18.addLayout(self.gridLayout_17, 0, 0, 1, 1)


        self.gridLayout_16.addWidget(self.groupBox_6, 0, 0, 1, 1)


        self.gridLayout_28.addLayout(self.gridLayout_16, 3, 0, 2, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_6 = QGridLayout(self.groupBox_2)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.pushButton_User_clear = QPushButton(self.groupBox_2)
        self.pushButton_User_clear.setObjectName(u"pushButton_User_clear")

        self.gridLayout_5.addWidget(self.pushButton_User_clear, 0, 0, 1, 1)

        self.textEdit_User = QTextEdit(self.groupBox_2)
        self.textEdit_User.setObjectName(u"textEdit_User")
        font1 = QFont()
        font1.setPointSize(12)
        self.textEdit_User.setFont(font1)
        self.textEdit_User.setReadOnly(True)

        self.gridLayout_5.addWidget(self.textEdit_User, 1, 0, 1, 1)


        self.gridLayout_6.addLayout(self.gridLayout_5, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.groupBox_2, 0, 0, 1, 1)


        self.gridLayout_28.addLayout(self.gridLayout_4, 3, 1, 2, 2)

        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_9 = QGridLayout(self.groupBox_3)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.pushButton_FeedBack_clear = QPushButton(self.groupBox_3)
        self.pushButton_FeedBack_clear.setObjectName(u"pushButton_FeedBack_clear")

        self.gridLayout_8.addWidget(self.pushButton_FeedBack_clear, 0, 0, 1, 1)

        self.textEdit_FeedBack = QTextEdit(self.groupBox_3)
        self.textEdit_FeedBack.setObjectName(u"textEdit_FeedBack")
        self.textEdit_FeedBack.setFont(font1)
        self.textEdit_FeedBack.setReadOnly(True)

        self.gridLayout_8.addWidget(self.textEdit_FeedBack, 1, 0, 1, 1)


        self.gridLayout_9.addLayout(self.gridLayout_8, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.groupBox_3, 0, 0, 1, 1)


        self.gridLayout_28.addLayout(self.gridLayout_7, 4, 3, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1000, 23))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"UDP\u8fde\u63a5\u4e0e\u8bbe\u5907\u521d\u59cb\u5316", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u673a\u7aef\u53e3\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u5907ID\uff1a", None))
        self.pushButton_Init.setText(QCoreApplication.translate("MainWindow", u"\u521d\u59cb\u5316\u8bbe\u5907UDP", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u4f4d\u673aIP\uff1a", None))
        self.pushButton_CMD_CX.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001\u67e5\u8be2\u547d\u4ee4", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u673aIP\uff1a", None))
        self.pushButton_CMD_DeviceInfo.setText(QCoreApplication.translate("MainWindow", u"\u52a0\u8f7d\u8bbe\u5907\u4fe1\u606f", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u4f4d\u673a\u7aef\u53e3\uff1a", None))
        self.comboBox_DeviceID.setItemText(0, QCoreApplication.translate("MainWindow", u"1", None))
        self.comboBox_DeviceID.setItemText(1, QCoreApplication.translate("MainWindow", u"2", None))
        self.comboBox_DeviceID.setItemText(2, QCoreApplication.translate("MainWindow", u"3", None))
        self.comboBox_DeviceID.setItemText(3, QCoreApplication.translate("MainWindow", u"4", None))
        self.comboBox_DeviceID.setItemText(4, QCoreApplication.translate("MainWindow", u"5", None))
        self.comboBox_DeviceID.setItemText(5, QCoreApplication.translate("MainWindow", u"6", None))
        self.comboBox_DeviceID.setItemText(6, QCoreApplication.translate("MainWindow", u"7", None))
        self.comboBox_DeviceID.setItemText(7, QCoreApplication.translate("MainWindow", u"8", None))
        self.comboBox_DeviceID.setItemText(8, QCoreApplication.translate("MainWindow", u"9", None))
        self.comboBox_DeviceID.setItemText(9, QCoreApplication.translate("MainWindow", u"10", None))

        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u5907\u4fe1\u606f\uff1a", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e\u53c2\u6570", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u89e6\u53d1\u95f4\u9694\uff1a", None))
        self.checkBox_Param_SC_DOWM.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u964d\u6cbf", None))
        self.checkBox_Param_SR_UP.setText(QCoreApplication.translate("MainWindow", u"\u4e0a\u5347\u6cbf", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u51fa\u89e6\u53d1\uff1a", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\u7070\u5ea6\u7b49\u7ea7\uff081-16\uff09\uff1a", None))
        self.checkBox_Param_SC_UP.setText(QCoreApplication.translate("MainWindow", u"\u4e0a\u5347\u6cbf", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u89e6\u53d1\uff1a", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u7247\u9891\u7387\uff08Hz\uff09\uff1a", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u89e6\u53d1\u5ef6\u65f6\uff1a", None))
        self.checkBox_Param_SR_DOWM.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u964d\u6cbf", None))
        self.pushButton_CMD_SetParam.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001\u8bbe\u7f6e\u53c2\u6570\u547d\u4ee4", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"\u52a0\u8f7d\u56fe\u50cf\u529f\u80fd", None))
        self.pushButton_ChooseBin.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9Bin\u6587\u4ef6", None))
        self.pushButton_SendTwo.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001\u4e8c\u503c", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u7247\u8d77\u59cb\u52a0\u8f7d\u4f4d\u7f6e", None))
        self.pushButton_SendEight.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001\u7070\u5ea6", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6\u5939\u5185\u56fe\u7247\u6570\u91cf\uff1a", None))
        self.pushButton_ChooseEightPic.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u516b\u4f4d\u7070\u5ea6\u6587\u4ef6\u5939", None))
        self.pushButton_ChooseTwoPic.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u4e8c\u503c\u56fe\u50cf\u6587\u4ef6\u5939", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001\u56fe\u7247\u6570\u91cf(\u5f20\u6570)", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001\u6570\u7ec4Demo", None))
        self.pushButton_SendBin.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001Bin", None))
        self.pushButton_SendChar.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001\u6570\u7ec4", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"\u6570\u7ec4Demo-\u56fe\u7247\u5bbd\u548c\u9ad8\uff1a", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"\u64ad\u653e\u64cd\u4f5c", None))
        self.comboBox_CMD_Play.setItemText(0, QCoreApplication.translate("MainWindow", u"\u5185\u90e8\u5355\u6b21", None))
        self.comboBox_CMD_Play.setItemText(1, QCoreApplication.translate("MainWindow", u"\u5185\u90e8\u5faa\u73af", None))
        self.comboBox_CMD_Play.setItemText(2, QCoreApplication.translate("MainWindow", u"\u5916\u90e8\u5355\u6b21", None))
        self.comboBox_CMD_Play.setItemText(3, QCoreApplication.translate("MainWindow", u"\u5916\u90e8\u5faa\u73af", None))
        self.comboBox_CMD_Play.setItemText(4, QCoreApplication.translate("MainWindow", u"\u53ef\u53d8\u5e8f\u5217\u5185\u90e8\u5355\u6b21", None))
        self.comboBox_CMD_Play.setItemText(5, QCoreApplication.translate("MainWindow", u"\u53ef\u53d8\u5e8f\u5217\u5185\u90e8\u5faa\u73af", None))
        self.comboBox_CMD_Play.setItemText(6, QCoreApplication.translate("MainWindow", u"\u53ef\u53d8\u5e8f\u5217\u5916\u90e8\u5355\u6b21", None))
        self.comboBox_CMD_Play.setItemText(7, QCoreApplication.translate("MainWindow", u"\u53ef\u53d8\u5e8f\u5217\u5916\u90e8\u5faa\u73af", None))

        self.label_19.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u7247\u5f20\u6570", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u4f4d\u7f6e", None))
        self.pushButton_CMD_PlayStop.setText(QCoreApplication.translate("MainWindow", u"\u6682\u505c", None))
        self.pushButton_CMD_Stop.setText(QCoreApplication.translate("MainWindow", u"\u4e2d\u6b62", None))
        self.pushButton_CMD_Play.setText(QCoreApplication.translate("MainWindow", u"\u64ad\u653e", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"\u5176\u4ed6\u64cd\u4f5c", None))
        self.pushButton_CMD_UPDOWM.setText(QCoreApplication.translate("MainWindow", u"\u4e0a\u4e0b\u7ffb\u8f6c", None))
        self.pushButton_CMD_DateReverse.setText(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u53cd\u5411", None))
        self.pushButton_CMD_SoftCF.setText(QCoreApplication.translate("MainWindow", u"\u8f6f\u4ef6\u89e6\u53d1", None))
        self.pushButton_CMD_DMDFloat.setText(QCoreApplication.translate("MainWindow", u"DMD-Float", None))
        self.pushButton_CMD_Reset.setText(QCoreApplication.translate("MainWindow", u"DMD-\u590d\u4f4d", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("MainWindow", u"\u81ea\u5b9a\u4e49\u547d\u4ee4", None))
        self.pushButton_SendZDYCmd.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001\u81ea\u5b9a\u4e49\u547d\u4ee4", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e\u5e8f\u5217", None))
        self.pushButton_CMD_SetSequence.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e\u5e8f\u5217", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u7528\u6237\u64cd\u4f5c\u4e0e\u64cd\u4f5c\u7ed3\u679c", None))
        self.pushButton_User_clear.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u9664", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\u4e0b\u4f4d\u673a\u53cd\u9988\u4fe1\u606f", None))
        self.pushButton_FeedBack_clear.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u9664", None))
    # retranslateUi

