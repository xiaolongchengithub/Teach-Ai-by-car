from carLib.thinkland_rpi_camera_client import Camera
from carLib.thinkland_rpi_car_client import Car
from aiLib.thinkland_rpi_ai import  Ai
import cv2


class aiCamera():
    """
    现在只是针对windows
    """
    def __init__(self ,ip):
        print("init camera")
        self.camera = Camera()

        self.camera.connect_http(ip) ##Ip 需要根据实际进行修改（树莓派的Ip）
        self.camera.start_receive_image_server()

        self.ai = Ai(classes="./aiLib/coco.names",config ="./aiLib/yolov3.cfg",weight = "./aiLib/yolov3.weights")

    def ai_show(self):
        while True:
            pic     = self.camera.take_picture()
            _,ret,_ = self.ai.find_object()
            cv2.imshow("ai",ret)
            cv2.waitKey(1)
