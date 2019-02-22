import socket
import cv2
import threading
import struct
import numpy
import time
import cv2 as cv
import cv2
import urllib
import numpy as np
import urllib.request
import numpy as np


"""
模块功能：从树莓派中获取图片
#利用Mjpg_treamer 服务其，获树莓派中获取数据流，转换为OPENCV格式的图片
"""
class Camera:
    def __init__(self):
        print('init the mjpg_streamer')
        self.__Show_Flag = False

    def connect_http(self,port):
        """
        *function:socket_connect
        功能：连接远程的 mjpg_streamer服务器
        ________
        Parameters
        * port : string
        - 输入服务器的Ip地址，例如""172.16.10.227""
        例如 test = Camera(),test.connect_http("172.16.10.227")
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
        self.__SHOW = True
        while self.__SHOW:
            bytes += self.stream.read(1024)
            a = bytes.find(b'\xff\xd8')
            b = bytes.find(b'\xff\xd9')
            if a != - 1 and b != -1:
                jpg = bytes[a:b + 2]
                bytes = bytes[b + 2:]
                self.image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), 1)
                if self.__Show_Flag:
                    cv2.imshow("Camera",self.image)
                    cv2.waitKey(1)

    def open_window(self):
        """
        *function:show_window
        功能：进行图片显示
        ________
        Parameters
        * None
        ————
        Returns
        -------
        * None
        """
        self.__Show_Flag = True

    def close_window(self):
        """
        *function:show_window
        功能：关闭窗口
        ________
        Parameters
        * None
        ————
        Returns
        -------
        * None
        """
        self.__Show_Flag = False

    def start_receive_image_server(self):
        """
        *function:start_receive_image_server
        功能：开启接受图片的线程
       例如: receiveImg = Camera();receiveImg.connect_http("172.16.10.227");receiveImg.start_receive_image_server()
        ________
        Parameters
        * None
        ————
        Returns
        -------
        * None
        """

        self.showThread = threading.Thread(target=self.socket_get_image_thread())
        self.showThread.start()
        time.sleep(1) #等待图像送达

    def show_image(self, mat , window_name = "rpi"):
        """
        *function:show_image
        功能：打开一个窗口进行图片显示
        例如：        import cv2
                      img = cv2.imread("c://test.jpg")
                      camera = Camera()
                      camera.show_image(img)
        ________
        Parameters
        *mat：图像数据，插入一张图片数据
        ————
        Return
        *None
         """
        cv2.imshow(window_name, mat)
        cv2.waitKey(1)

    def set_ai(self , ai):
        """
        *function:set_ai
        功能：引入yolo类
        ________
         Parameters
        *ai：thinkland_rpi_ai_yolov3模块中的AiYolo类
        """
        self.Ai = ai

    def close_receive_image_server(self):
        """
        *function:close_receive_image_server
        功能：关闭视频流服务线程
        ________
        Parameters
        * None
        ————
        Returns
        -------
        * None
        """
        self.SHOW = False

    def take_picture(self):
        """
        *function:takePicture
        功能：从视频流中获取一张图片
        ________
        Parameters
        * None
        ————
        Returns
        -------
        * Mat
        返回一张图片
        """
        return self.image

    def demo_connect_rpi_sever():
        """
        *function:demo_connect_rpi_sever
        功能：连接树莓派的服务
        ________
        Parameters
        * None
        ————
        Returns
        -------
        * None
        """
        receiveImg = Camera()
        receiveImg.connect_http("172.16.10.227")#Ip为树莓派的Ip
        receiveImg.start_receive_image_server()#启动数据获取线程
        receiveImg.open_window()#实时图像显示

"""
@@@@例子：
#获取树莓派的摄像头数据流
"""
if __name__ == "__main__":
    Camera.demo_connect_rpi_sever()





