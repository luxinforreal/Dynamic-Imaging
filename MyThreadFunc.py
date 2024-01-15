# encoding: utf-8

import time
import threading
import inspect
import ctypes


class MyThreadFunc(object):
    '''
    手动终止线程的方法
    '''
    def __init__(self, func):
        self.myThread = threading.Thread(target=func)

    def start(self):
        print('线程启动')
        self.myThread.start()

    def stop(self):
        print('线程终止')
        try:
            for i in range(5):
                self._async_raise(self.myThread.ident, SystemExit)
                time.sleep(1)
        except Exception as e:
            print(e)

    def _async_raise(self, tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")