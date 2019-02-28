from carLib.thinkland_rpi_camera_client import Camera
from aiLib.thinkland_rpi_ai import  Ai
from carLib.thinkland_rpi_car_client import Car
import cv2
import time
import threading
from aiLib.thinkland_rpi_algorithm import Algrithm


class Tracking():
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
        self.camera.open_window()

        self.car = Car()
        self.car.connect(ip)

        self.algithm = Algrithm()

    def get_line(self ,frame = cv2.imread('line.jpg')):
        self.point = self.algithm.line(frame)
        print(self.point)
        return self.point

    def move_line_tracking(self, speed = 4, times = 1):
        # self.car.turn_servo_camera_vertical(35)
        # self.car.turn_servo_camera_horizental(90)
        while True:
            pic = self.camera.take_picture()
            pt = self.get_line(pic)
            print(type(pt))
            x = pt[0]
            print(type(x))
            print(x)
            if 250 < x < 380:
                self.car.run_forward(speed , times)
            elif x < 250:
                print("spin right")
                self.car.turn_left(speed*0.6,times)
            elif x > 380:
                print("spin left")
                self.car.turn_right(speed*0.6,times)

def main():
    """
    例子
    """
    track = Tracking()
    track.move_line_tracking()

if __name__ == "__main__":
    main()
