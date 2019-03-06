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

    ai = Ai()

    while True:
        pic = camera.take_picture()
        ret, names, box = ai.find_object(pic)
        cv2.imshow("ai", ret)
        k = cv2.waitKey(1)
        if k == 27:  # wait for ESC key to exit
            cv2.destroyAllWindows()
            break

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

    ai = Ai()
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
    str = input('输入树莓派的IP:')
    demo_ai_camera(str)

if __name__ == "__main__":
    main()


