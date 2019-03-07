"""
    摄像机封装类，通过创建Camera类示例，调用相应api可以获得摄像机视频流并显示。
    小车服务端运行了一个Mjpg_streamer串流服务，该服务会将摄像机的视频通过http协议
    进行传输。当我们连接到这个服务的ip和port，就可以接收到流媒体数据，我们再将数据
    解码并显示。
    提示：由于macOS系统下opencv不支持在fork的线程和进程中刷新GDI,并且会引起程序崩溃。
         所以为了兼容macOS系统只有将视频显示放到主线程中，会阻塞主线程
"""
# Todo: 改进图像更新方式

import threading
import cv2
import urllib
import urllib.request
import numpy as np
import time


__authors__ = 'xiao long & xu lao shi'
__version__ = 'version 0.02'
__license__ = 'Copyright...'


class HttpMixin:
    """http功能Mixin
    """
    url_streamer = 'http://172.16.10.227:8080/?action=streamer'

    def connect_server(self, ip, port=8080):
        """连接服务器
        """
        url = 'http://{}:{}/?action=streamer'.format(ip, port)

        self.stream = urllib.request.urlopen(url)

    def start_receive(self):
        """开始接收数据
        """
        receiveThread = threading.Thread(target=self.receive_data)
        receiveThread.start()

    def receive_data(self):
        """接收数据
        """
        time.sleep(2)
        print("start receive")
        buffer = b''
        while True:
            buffer += self.stream.read(1024)
            data_header = buffer.find(b'\xff\xd8')
            data_end = buffer.find(b'\xff\xd9')
            if data_header != - 1 and data_end != -1:
                jpg = buffer[data_header:data_end + 2]
                buffer = buffer[data_end + 2:]
                image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), 1)
                self.data_handler(image)

    def data_handler(self, data):
        """处理数据
        由子类定义具体功能
        Parameters
        -----------
        data:
            - 接收到的解析数据
        Return
        ---------

        """
        pass


class Camera(HttpMixin):
    """摄像机类
    """

    def __init__(self):
        self.__Show_Flag = False
        self.ai = None
        self._image = np.array([])

    def data_handler(self, data):
        """处理从小车摄像获取的图片

        Parameters
        * data: numpy array
            - 从小车摄像机数据

        Returns
        -------
        * None
        """
        self._image = data

    def play(self):
        """播放摄像头视频,可以通过ESC键关闭
        """
        while not self._image.size:
            time.sleep(1)

        while True:
            try:
                cv2.imshow("Camera", self._image)
                k = cv2.waitKey(1)
                if k == 27:  # wait for ESC key to exit
                    cv2.destroyAllWindows()
                    self._image = np.array([])
                    break
            except:
                pass

    def set_ai(self, ai_yolo):
        """引入yolo类

        Parameters
        --------------
        * ai：AiYolo类
            - thinkland_rpi_ai_yolov3模块中的AiYolo类

        """
        self.ai = ai_yolo

    def take_picture(self):
        """控制摄像机拍照

        Parameters
        -----------
        * None

        Returns
        -------
        * numpy array
        返回一张图片
        """

        while not self._image.size:
            time.sleep(1)
        return self._image

    @staticmethod
    def save_picture(mat, path):
        """从视频流中获取一张图片

        Parameters
        * mat: numpy array
            - 图像数据
        * path: str
            - 图像保存地址
        -----------------
        Returns
        -----------------
        * Mat
        返回一张图片
        """
        cv2.imwrite(path, mat)

    @staticmethod
    def demo_play_camera_video():
        """播放小车摄像头视频
        """
        camera = Camera()
        camera.connect_server("172.16.10.227")
        camera.start_receive()
        camera.play()

    @staticmethod
    def demo_take_picture():
        """控制摄像机拍照，并保存
        """
        camera = Camera()
        camera.connect_server("172.16.10.227")
        camera.start_receive()
        image = camera.take_picture()
        camera.save_picture(image, './phone.jpg')  # 保存到当前目录下test.jpg文件


def main():
    demo_index = int(input("请选择演示demo(0:显示摄像头视频，1：显示并保存一张图到本地):"))

    if demo_index == 0:
        print(" 按下ECS键可关停止播放")
        Camera.demo_play_camera_video()
    elif demo_index == 1:
        Camera.demo_take_picture()


if __name__ == "__main__":
    main()
