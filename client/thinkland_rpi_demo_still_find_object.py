import platform
type = platform.platform()
print(type)
if 'Mac' in type:
    from carLib.thinkland_rpi_camera_client import Camera
    from carLib.thinkland_rpi_car_client import Car
    from aiLib.thinkland_rpi_ai import  Ai
    from aiLib.thinkland_rpi_speaker import Speaker
else:
    from client.carLib.thinkland_rpi_camera_client import Camera
    from client.carLib.thinkland_rpi_car_client import Car
    from client.aiLib.thinkland_rpi_ai import  Ai
    from client.aiLib.thinkland_rpi_speaker import Speaker

import time
import cv2
from pynput import keyboard
from pynput.keyboard import Key
import threading

"""
停止按钮
"""
STOP_FLAGE = False  # 遇到特殊按钮，则停止demo演示


def on_press(key):
    global STOP_FLAGE
    try:
        common = ('alphanumeric key  {0} pressed'.format(key.char))
    except AttributeError:
        if key == Key.space:
            print('stop demo'.format(
                key))
            print('stop')
            STOP_FLAGE = True  # 遇到特殊按钮，则停止demo演示



def listenser():
    with keyboard.Listener(
            on_press= on_press) as listener:
        listener.join()

def start_listenser_thread():
    threadId = threading.Thread(target= listenser)
    threadId.start()


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
    global STOP_FLAGE

    camera = Camera()
    camera.connect_server(ip)
    camera.start_receive()
    camera.thread_play()

    car = Car(ip)
    ai = Ai()

    speaker = Speaker()

    car.turn_servo_camera_vertical(30)

    for angle in range(20, 180, 20):
        car.turn_servo_camera_horizental(angle)
        time.sleep(2)  #图像稳定时间
        picture = camera.take_picture()
        frame, names, _ = ai.find_object(picture)

        if STOP_FLAGE:
            return

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
    print(type(object))

    global STOP_FLAGE

    camera = Camera()
    camera.connect_server(ip)
    camera.start_receive()
    camera.thread_play()

    car = Car(ip)
    ai = Ai()

    speaker = Speaker()


    for pos in range(25,55,15):
        car.turn_servo_camera_vertical(pos)
        for angle in range(20, 180, 20):
            car.turn_servo_camera_horizental(angle)
            time.sleep(2)  #图像稳定时间
            picture = camera.take_picture()
            frame, names, _ = ai.find_object(picture)

            if STOP_FLAGE:
                return

            print(names)
            for item in names:
                if item == object:
                    speaker.say("find a")
                    speaker.say(item)
                    cv2.imshow('result', frame)
                    cv2.waitKey(0)
                    return

if __name__ == "__main__":
    start_listenser_thread()
    str = input('输入树莓派的IP:')
    demo_shaking_camera_find_object1(str,"cup")


