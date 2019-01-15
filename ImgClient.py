import socket
import cv2
import threading
import struct
import numpy
import time

import cv2 as cv
import numpy as np
import dialog as dlg
import ai


imglist = []
frame   = []
global dg
global camera
global oj

class Camera_Connect_Object:
    def __init__(self, D_addr_port=["172.16.10.227", 12345]):
        self.resolution = [640, 480]
        self.addr_port = D_addr_port
        self.src = 888 + 15  # 双方确定传输帧数，（888）为校验值
        self.interval = 0  # 图片播放时间间隔
        self.img_fps = 15  # 每秒传输多少帧数



    def Set_socket(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def Socket_Connect(self):
        self.Set_socket()
        self.HOST = '172.16.10.227'  # or 'localhost'
        self.PORT = 12345
        self.ADDR = (self.HOST, self.PORT)
        self.client.connect(self.ADDR)
        print("IP is %s:%d" % (self.addr_port[0], self.addr_port[1]))

    def RT_Image(self):
        # 按照格式打包发送帧数和分辨率
        global   frame
        global   imglist
        global   mutex
        self.name = self.addr_port[0] + " Camera"
        self.client.send(struct.pack("lhh", self.src, self.resolution[0], self.resolution[1]))
        while (1):
            info = struct.unpack("lhh", self.client.recv(8))
            buf_size = info[0]  # 获取读的图片总长度
            if buf_size:
                try:
                    self.buf = b""  # 代表bytes类型
                    temp_buf = self.buf
                    while (buf_size):  # 读取每一张图片的长度
                        temp_buf = self.client.recv(buf_size)
                        buf_size -= len(temp_buf)
                        self.buf += temp_buf  # 获取图片
                        data = numpy.fromstring(self.buf, dtype='uint8')  # 按uint8转换为图像矩阵
                        self.image = cv2.imdecode(data, 1)  # 图像解码
                    mutex.acquire()
                    imglist.append(self.image)
                    mutex.release()
                except:
                    pass;
                finally:
                    pa = 1


    def Get_Data(self, interval):
        showThread = threading.Thread(target=self.RT_Image)
        showThread.start()

    def takePicture():
        global mutex
        if len(imglist) > 0:
            mutex.acquire()
            self.pic = imglist.pop()
            mutex.release()
            return pic

def findObjct(img):
    return oj.GetRect(img)

id = 0
def imgTest(obj):
    global  id
    strNmae = "D://%d.jpg" % (id)
    strNmae = str(strNmae)
    cv2.imwrite(strNmae,frame)
    id =  id + 1
    if len(imglist) > 0:
        rec,names = findObjct(frame)
        print(names)
        for i in names:
            if i == obj:
                return True
    return False



def DataDeal():
    global imglist
    global frame
    global dg
    global  mutex
    global oj
    global imgo
    checkObj = ai.ObjectClass()
    while True:
        # print(len(imglist))
        mutex.acquire()
        if len(imglist) > 0:
            frame = imglist.pop()
            mutex.release()
            retFrame = checkObj.FindObject(frame)
            dg.SetImgInput(retFrame)
        else:
            mutex.release()
        mutex.acquire()
        if len(imglist) > 20:
            l = len(imglist)
            l = l-10
            del imglist[-l:]
            mutex.release()
        else:
            mutex.release()
        time.sleep(0.01)

def connectSever():
    global  oj
    global  imgo
    global  img
    global  mutex

    img = cv.imread("D://dog.jpg")
    mutex = threading.Lock()
    oj = ai.ObjectClass()
    camera = Camera_Connect_Object()
    camera.addr_port[0] = "服务端的ip"
    camera.addr_port = tuple(camera.addr_port)
    camera.Socket_Connect()
    camera.Get_Data(camera.interval)



    dataThread = threading.Thread(target=DataDeal)
    dataThread.start()

def setInput(d):
    global  dg
    dg = d

