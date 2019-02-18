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

#模块功能：从树莓派中获取图片
#利用Mjpg_treamer 服务其，获取其数据流，转换为opencv格式的图片


class Camera:
    def __init__(self):
        print('init the mjpg_streamer')
        self.imglist = []

    def socket_connect(self,port):
        """
        *function:socket_connect
        功能：连接远程的 mjpg_streamer服务器
        ________
        Parameters
        * port : string
        - 输入服务器的Ip地址，例如""172.16.10.227""
        ————
        Returns
        -------
        * None
        """
        connectPort = 'http://%s:8080/?action=stream'%port
        self.stream = urllib.request.urlopen(connectPort)

    def socket_get_image_thread(self):
        # 按照格式打包发送帧数和分辨率
        """
        *function:socket_get_image_thread
        功能：从服务器获取，并解密获取图片
        ________
        Parameters
        * None
        ————
        Returns
        -------
        * None
        """
        bytes = b''
        while True:
            bytes += self.stream.read(1024)
            a = bytes.find(b'\xff\xd8')
            b = bytes.find(b'\xff\xd9')
            if a != - 1 and b != -1:
                jpg = bytes[a:b + 2]
                bytes = bytes[b + 2:]
                self.image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), 1)
                cv2.imshow("img",self.image)
                cv2.waitKey(1)
                # mutex.acquire()
                self.imglist.append(self.image)
                # mutex.release()

    def start_receive_image_server(self):
        """
        *function:start_receive_image_server
        功能：开启接受图片的线程
        ________
        Parameters
        * None
        ————
        Returns
        -------
        * None
        """
        self.showThread = threading.Thread(target=self.RT_Image)
        self.showThread.start()

    def take_picture():
        """
        *function:takePicture
        功能：从视频流中获取一张图片
        ________
        Parameters
        * None
        ————
        Returns
        -------
        * None
        """
        if len(self.imglist) > 0:
            # mutex.acquire()
            self.pic = imglist.pop()
            # mutex.release()
            return pic

receiveImg = Camera_Connect_Object()
receiveImg.Socket_Connect("172.16.10.227")
receiveImg.Get_Data()
