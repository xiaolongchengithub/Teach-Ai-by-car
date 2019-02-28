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

__authors__ = 'xiao long & xu lao shi'
__version__ = 'version 0.02'
__license__ = 'Copyright...'

class Camera:
    """
    模块功能：从树莓派中获取图片
    利用Mjpg_treamer 服务其，获树莓派中获取数据流，转换为OPENCV格式的图片
    *connect_http                   远程连接
    *socket_get_image_thread        获取图像数据
    *open_window                    打开显示窗口
    *close_window 关闭显示窗口
    *start_receive_image_server 启动图像采集线程
    *show_image 图像显示
    *set_ai 引入图像识别功能
    *take_picture 采集一张图像数据
    *save_picture 保存一张图像
    """

    def __init__(self):
        self.__Show_Flag = False

    def connect_http(self,port = "172.16.10.227"):
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
        print('init the mjpg_streamer')

    def http_close(self):
        urllib.request.urlcleanup()

    def http_get_image_thread(self):
        # 按照格式打包发送帧数和分辨率
        """
        *function:http_get_image_thread
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

        self.showThread = threading.Thread(target=self.http_get_image_thread)
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

    def save_picture(self , mat, path):
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
        cv2.imwrite(path,mat)

    @staticmethod
    def demo_collect_picture_windowsOrlinux():
        """
        启动这个例子之前需要在树莓派上启动服务 python thinkland_rpi_sever.py
        在windows/linux上使用此例子
        如果不open_window，Ios系统也可以按照这个方式调用。IOS在系统图像显示的时候会出现卡死的问题
        """
        camera = Camera()
        camera.connect_http("172.16.10.227") ##Ip 需要根据实际进行修改（树莓派的Ip）
        camera.start_receive_image_server()
        camera.open_window()

    @staticmethod
    def demo_only_take_picture():
        """
        不实时显示图像，截取当前图片，并保存
        """
        camera = Camera()
        camera.connect_http("172.16.10.227") ##Ip 需要根据实际进行修改（树莓派的Ip）
        camera.start_receive_image_server()

        picture = camera.take_picture()
        camera.save_picture(picture,'./test.jpg')


    @staticmethod
    def demo_collect_picture_windowsOrlinux_save_one_picture():
        """
        启动服务，并截取一张张片，并保存
        """
        camera = Camera()
        camera.connect_http("172.16.10.227") ##Ip 需要根据实际进行修改（树莓派的Ip）
        camera.start_receive_image_server()
        camera.open_window()

        picture = camera.take_picture()
        camera.save_picture(picture,'./test.jpg')


    @staticmethod
    def demo_show_picture_ios():
        """
        在IOS上实时显示树莓派上的图像流
        """
        global ios_camera

        mainThread = threading.Thread(target=window)
        mainThread.start()
        ios_camera = Camera()
        ios_camera.connect_http("172.16.10.227")
        ios_camera.http_get_image_thread()



def window():
    global ios_camera
    while True:
        input("Press Enter to open camera")
        ios_camera.open_window()
        input("Press Enter again to close it")
        ios_camera.close_window()

"""
@@@@例子：
#获取图片
"""

camera_learning_status = 0  #相机学习等级 0 :在客服端实时显示图像的例子
                            #相机学习等级 1 :在客服端实时显示图像，并从中截取一张图片用来显示
                            #相机学习等级 2 ：不现实图像，并截取一张图像
                            #相机学习等级 3： IOS系统实时显示


if __name__ == "__main__":
    """
    从树莓派中获取视频流，为了排除干扰，最好把电脑上的杀毒软件等关掉
    """

    camera_learning_status = int(input("输入相机学习等级(0:图像显示，1：显示并保存一张图到本地，2：不显示，只保存图像，3：Ios图像显示):"))
    print(camera_learning_status)
    if camera_learning_status == 0:
        Camera.demo_collect_picture_windowsOrlinux()
    elif camera_learning_status == 1:
        Camera.demo_collect_picture_windowsOrlinux_save_one_picture()
    elif  camera_learning_status == 2:
        Camera.demo_only_take_picture()
    elif  camera_learning_status == 3:
        Camera.demo_show_picture_ios()




