from carLib.thinkland_rpi_camera_client import Camera
from aiLib.thinkland_rpi_ai import  Ai
import cv2
import time
import threading
from aiLib.thinkland_rpi_speaker import Speaker

def demo_ai_camera(ip):
    """
    智能相机的构建，实时识别相机中的物体

    Parameter
    ----
    *ip：string
        -树莓派的Ip
    """
    camera = Camera()
    camera.connect_server(ip)
    camera.start_receive()

    ai = Ai(classes="./aiLib/coco/coco.names", config="./aiLib/coco/yolov3.cfg",
            weight="./aiLib/coco/yolov3.weights")

    while True:
        pic = camera.take_picture()
        ret, names, box = ai.find_object(pic)
        cv2.imshow("ai", ret)
        cv2.waitKey(1)

def demo_ai_camera_speaker(ip):
    """
    智能相机的构建，实时识别相机中的物体
    间隔一段时间，把识别的物体朗读出来

    Parameter
    --------
    *ip:string
       -树莓派的IP
    """
    camera = Camera()
    camera.connect_server(ip)
    camera.start_receive()

    ai = Ai(classes="./aiLib/coco/coco.names", config="./aiLib/coco/yolov3.cfg",
            weight="./aiLib/coco/yolov3.weights")
    speaker = Speaker()

    interval = 20
    times    = 0
    while True:
        pic = camera.take_picture()
        ret,names,box= ai.find_object(pic)

        cv2.imshow("ai", ret)
        cv2.waitKey(1)

        times = times + 1
        if times > interval:
            times = 0
            if len(names) > 0:
                speaker.say('i find')
            for item in names:
                speaker.say(item)
            if len(names) > 0:
                speaker.say('in the picture')

def main():
    """
    例子
    """
    demo_ai_camera("172.16.10.227")

if __name__ == "__main__":
    main()


