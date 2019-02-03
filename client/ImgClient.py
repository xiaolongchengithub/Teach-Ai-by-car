import socket
import cv2
import threading
import struct
import numpy
import time
import cv2 as cv
import algorithm as algori
import cv2
import urllib
import numpy as np
import urllib.request
import numpy as np
import dialog as dlg
from yolov3 import ai



imglist = []
frame   = []
global dg
global camera
global oj
global g_bshow
global g_control

class Camera_Connect_Object:
    def __init__(self, D_addr_port=["172.16.10.227", 12345]):
        print('init the mjpg_streamer')



    def Socket_Connect(self,port):
        connectPort = 'http://%s:8080/?action=stream'%port
        self.stream = urllib.request.urlopen(connectPort)


    def RT_Image(self):
        # 按照格式打包发送帧数和分辨率
        global   frame
        global   imglist
        global   mutex

        bytes = b''
        while True:
            bytes += self.stream.read(1024)
            a = bytes.find(b'\xff\xd8')
            b = bytes.find(b'\xff\xd9')
            if a != - 1 and b != -1:
                jpg = bytes[a:b + 2]
                bytes = bytes[b + 2:]
                self.image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), 1)
                mutex.acquire()
                imglist.append(self.image)
                mutex.release()



    def Get_Data(self):
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
    if len(imglist) > 0:
        rec,names = findObjct(frame)
        print(names)
        for i in names:
            if i == obj:
                return True
    return False
imgId = 0
def findLine():
    global imgId
    imgId = imgId + 1
    saveImage('./snap/%d.jpg'%imgId)
    return algori.line(frame)


def find():
    if len(imglist) > 0:
        rec,names = findObjct(frame)
    return names

global g_findObject
g_findObject = False
def DataDeal():
    global imglist
    global frame
    global dg
    global  mutex
    global oj
    global imgo
    global g_bshow
    global g_control
    checkObj = ai.ObjectClass()
    while True:
        # print(len(imglist))
        mutex.acquire()
        if len(imglist) > 0:
            frame = imglist.pop()
            mutex.release()
            if g_bshow:
                t1 = time.time()
                retFrame,names,box = checkObj.FindObject(frame)
                dg.setImgInput(retFrame)
                t2 = time.time()
                print(t2-t1)
                # for iname in names:
                #     if iname == 'cup':
                #         print('stop the car')
                #         g_control.stopAutoRun()

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


def connectSever(port):
    global  oj
    global  imgo
    global  img
    global  mutex

    img = cv.imread("D://dog.jpg")
    mutex = threading.Lock()
    oj = ai.ObjectClass()
    receiveImg = Camera_Connect_Object()
    receiveImg.Socket_Connect(port)
    receiveImg.Get_Data()
    dataThread = threading.Thread(target=DataDeal)
    dataThread.start()

def saveImage(path):
    global frame
    cv2.imwrite(path, frame)


def setInput(d,control,show = True):
    global  dg
    global  g_bshow
    global  g_control

    dg      = d
    g_bshow = show
    g_control = control

