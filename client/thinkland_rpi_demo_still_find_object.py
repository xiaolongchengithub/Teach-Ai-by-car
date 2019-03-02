from carLib.thinkland_rpi_camera_client import Camera
from carLib.thinkland_rpi_car_client import Car
from aiLib.thinkland_rpi_ai import  Ai
from aiLib.thinkland_rpi_speaker import Speaker
import time
import cv2

"""
例子：利用相机寻找物体
"""

def demo_shaking_camera_find_object(ip ,object):
    """
     控制相机的舵机寻找物体,保持相机上下方向固定，在水平方向进行旋转

     Parameter
     ---
     *object:string
         -要寻找的物体
    """
    assert (type(object) == str)
    assert(type(ip) == str)

    camera = Camera()
    camera.connect_server(ip)
    camera.start_receive()
    camera.thread_play()

    car = Car(ip)
    ai = Ai(classes="./aiLib/coco/coco.names", config="./aiLib/coco/yolov3.cfg", weight="./aiLib/coco/yolov3.weights")

    speaker = Speaker()

    car.turn_servo_camera_vertical(30)

    for angle in range(20, 180, 20):
        car.turn_servo_camera_horizental(angle)
        time.sleep(2)  #图像稳定时间
        picture = camera.take_picture()
        frame, names, _ = ai.find_object(picture)

        print(names)
        for item in names:
            if item == object:
                speaker.say("find a")
                speaker.say(item)
                cv2.imshow('result', frame)
                cv2.waitKey(0)
                return

def demo_shaking_camera_find_object1(ip ,object):
    """
     控制相机的舵机寻找物体,让相机上下水平进行旋转，寻找物体

     Parameter
     ---
     *object:string
         -要寻找的物体
    """
    assert (type(object) == str)
    assert(type(ip) == str)

    camera = Camera()
    camera.connect_server(ip)
    camera.start_receive()
    camera.thread_play()

    car = Car(ip)
    ai = Ai(classes="./aiLib/coco/coco.names", config="./aiLib/coco/yolov3.cfg", weight="./aiLib/coco/yolov3.weights")

    speaker = Speaker()

    for pos in range(25,55,15):
        car.turn_servo_camera_vertical(pos)
        for angle in range(20, 180, 20):
            car.turn_servo_camera_horizental(angle)
            time.sleep(2)  #图像稳定时间
            picture = camera.take_picture()
            frame, names, _ = ai.find_object(picture)

            print(names)
            for item in names:
                if item == object:
                    speaker.say("find a")
                    speaker.say(item)
                    cv2.imshow('result', frame)
                    cv2.waitKey(0)
                    return

if __name__ == "__main__":

    demo_shaking_camera_find_object1("172.16.10.227","cup")


