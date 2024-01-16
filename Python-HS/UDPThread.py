from PySide2.QtCore import QThread, Signal, QObject

from ctypes import *


class Mysignal(QObject):
    signal = Signal(str, int)


class udppthread(QThread):
    def __init__(self):
        QThread.__init__(self)

        self.Rec_BS = True
        self.Device_ID = 0
        self.XC_BS = False
        self.XC_Data = (c_ubyte * 32)()

        # 动态库
        self.lib = None

        # 信号
        self.FeedBack_TextEditShow = Mysignal()

    @staticmethod
    def str2Hex(data, length):
        strResult = ""
        for i in range(length):
            strResult += ""
            strResult += str(hex(data[i])[2:].zfill(2))
            strResult += " "
        return strResult

    def run(self):
        while self.Rec_BS:
            buff = (c_ubyte * 2048)()
            bufflen = self.lib.FL_DLP_HS_Reveive(self.Device_ID, buff)

            if bufflen != 0:
                Receive_Data = self.str2Hex(buff, bufflen)
                self.FeedBack_TextEditShow.signal.emit('Receive Data：', 0)
                self.FeedBack_TextEditShow.signal.emit(Receive_Data, 0)

                if self.XC_BS:
                    for i in range(bufflen):
                        self.XC_Data[i] = buff[i]

