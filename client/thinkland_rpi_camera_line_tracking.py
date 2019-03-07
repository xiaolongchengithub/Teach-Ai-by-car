from client.carLib.thinkland_rpi_camera_client import Camera
from client.aiLib.thinkland_rpi_ai import  Ai
from client.carLib.thinkland_rpi_car_client import Car
import cv2
from client.aiLib.thinkland_rpi_algorithm import Algrithm

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

def demo_line_algrithm(ip,speed,dis):
    """
    利用图像传统知识进行巡线,对图像进行二值化，选取组最大的轮廓的中心点。图像的长640，宽480。
     0  左转 250  直行 320  直行 380 右转  640

     Parameter
     --------
     * ip:string
        -树莓派的IP
     * speed:int
        -小车运行速度
     * dis：float
        -运行的时间，控制距离
    """
    #相机的初始化
    camera = Camera()
    camera.connect_server(ip)
    camera.start_receive()
    # camera.thread_play()
    #算法初始化
    algithm = Algrithm()
    #小车初始化
    car = Car(ip)

    global STOP_FLAGE
    while True:
        pic = camera.take_picture()
        pt = algithm.line(pic)
        x = pt[0]
        print(x)
        if 250 < x < 380:
            car.run_forward(speed, dis) #直行
        elif x < 250:
            print("spin left")
            car.turn_left(speed * 0.6, dis) #左转
        elif x > 380:
            print("spin right")
            car.turn_right(speed * 0.6, dis)#右转
        if STOP_FLAGE:
            return

######################################################################################

def demo_line_ai(ip, speed, dis):
    """
    利用训练数据进行巡线

    Param
    -----
    *ip: string
        -树莓的ip
    *speed: int
        -运行速度
    *dis: int
        -检测一次走的距离
    """
    #相机初始化
    camera = Camera()
    camera.connect_server(ip)
    camera.start_receive()
    # camera.thread_play()
    #车初始化
    car = Car(ip)
    #Ai初始化，自己训练的结果
    ai = Ai()

    global STOP_FLAGE
    while True:
        pic = camera.take_picture()#cv2.imread("./aiLib/line/line.jpg")#
        ret,name,box = ai.find_object(pic)
        cv2.imshow('test',ret)
        cv2.waitKey(1)
        # continue
        x = 0
        if len(name) == 0: #没有检测到线
            continue

        for item in name:
            if item == 'line':
                x = box[0][0]
                print(x, type(x))

        if 250 < x < 380:
            car.run_forward(speed, dis) #直行
        elif x < 250:
            print("spin right")
            car.turn_left(speed * 0.6, dis)#左转
        elif x > 380:
            print("spin left")
            car.turn_right(speed * 0.6, dis)#右转

        if STOP_FLAGE:
            return

def main():
    """
    例子
    """
    str = input('输入树莓派的IP')
    demo_line_algrithm(str,15,0.05)


if __name__ == "__main__":
    start_listenser_thread()
    main()
