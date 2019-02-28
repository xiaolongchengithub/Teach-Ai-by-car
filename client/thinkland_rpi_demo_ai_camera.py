from carLib.thinkland_rpi_camera_client import Camera
from aiLib.thinkland_rpi_ai import  Ai
import cv2
import time
import threading
from aiLib.thinkland_rpi_speaker import Speaker


class aiCamera():
    """
    现在只是针对windows llinux
    制作智能相机，识别视野中的物体
    """
    def __init__(self ,ip = "172.16.10.227"):
        """
        初始化，区别coco.names;yolov3.cfg;yolov3.weights文件放在aiLib文件夹中;
        启动相机服务


        Parameter
        --------
             --ip string类型，default "172.16.10.227" ，
        """
        print("init camera")
        self.camera = Camera()

        self.camera.connect_http(ip)
        self.camera.start_receive_image_server()
        self.ai = Ai(classes="./aiLib/coco.names",config ="./aiLib/yolov3.cfg",weight = "./aiLib/yolov3.weights")
        self.speaker = Speaker()

    def ai_show(self):
        """
        获取相机，实时检测，图像显示
        """
        while True:
            pic     = self.camera.take_picture()
            ret,names,_ = self.ai.find_object(pic)
            cv2.imshow("ai",ret)
            cv2.waitKey(1)

    def ai_show_speaker(self):
        """
        获取相机，实时检测，图像显示, 语音朗读
        """
        interval = 50  #间隔多少次，朗读一次
        times    = 0

        while True:
            pic     = self.camera.take_picture()
            ret,names,_ = self.ai.find_object(pic)
            cv2.imshow("ai",ret)
            cv2.waitKey(1)

            times = times + 1
            if times > interval:
                times = 0
                if len(names) > 0:
                    self.speaker.say('i find')
                for item in names:
                    self.speaker.say(item)
                if len(names) > 0:
                    self.speaker.say('in the picture')

    def start_thread_ai_camera(self):
        """
        启动线程
        """
        self.mainThread = threading.Thread(target=self.ai_show)
        self.mainThread.start()

    def start_thread_ai_camera_speaker(self):
        """
        启动线程
        """
        self.mainThread = threading.Thread(target=self.ai_show_speaker())
        self.mainThread.start()

    @staticmethod
    def demo():
        """
        制作智能相机
        """
        camera = aiCamera("172.16.10.227")
        time.sleep(1)
        camera.start_thread_ai_camera()

def main():
    """
    例子
    """
    aiCamera.demo()

if __name__ == "__main__":
    main()


