from carLib.thinkland_rpi_camera_client import Camera
from carLib.thinkland_rpi_car_client import Car
from aiLib.thinkland_rpi_ai import  Ai
import random
import threading
import time
import cv2
from aiLib.thinkland_rpi_speaker import Speaker

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

CRUSING_FLOG  = True

def Cruising(car,speed=4):
    """
    Demonstrates a cruising car that avoids obstacles in a room

    * Use infrared sensors and ultrasonic sensor to gauge obstacles
    * Use LED lights to indicate running/turning decisions
    """
    global CRUSING_FLOG
    global STOP_FLAGE

    try:
        while True:
            if STOP_FLAGE == True:
                car.stop_all_wheels()
                print('Cruising over .............................................')
                break

            if CRUSING_FLOG == False:
                car.stop_all_wheels()
                print('Cruising over .............................................')
                break

            obstacle_status_from_infrared = car.obstacle_status_from_infrared()
            should_turn = True
            print(obstacle_status_from_infrared)
            if obstacle_status_from_infrared == 'clear':
                should_turn = False
                obstacle_status_from_ultrasound = \
                    car.obstacle_status_from_ultrasound()
                if obstacle_status_from_ultrasound == 'clear':
                    car.run_forward(speed)
                elif obstacle_status_from_ultrasound == 'approaching_obstacle':
                    car.run_forward(speed * 0.5)
                else:
                    should_turn = True
            if should_turn:
                car.run_reverse(speed,duration=0.1)
                if obstacle_status_from_infrared == 'only_right_blocked':
                    car.spin_left(2*speed,duration=random.uniform(0.25, 1.0))
                elif obstacle_status_from_infrared == 'only_left_blocked':
                    car.spin_right(2*speed,duration=random.uniform(0.25, 1.0))
                else:
                    car.spin_right(2*speed,duration=random.uniform(0.25, 1.0))
    except KeyboardInterrupt:
         print('KeyboardInterrupt')
         car.stop_all_wheels()

def find_object(ip,camera,ai,object):
    global CRUSING_FLOG
    global STOP_FLAGE
    car = Car(ip)
    car.turn_servo_camera_vertical(30)
    angle = [40,70,100,130,160]

    while True:
        for ita in angle:
            car.turn_servo_camera_horizental(ita)
            time.sleep(0.2)
            pic = camera.take_picture()
            cv2.imshow('pic',pic)
            cv2.waitKey(1)
            ret, names, _ = ai.find_object(pic)

            if STOP_FLAGE == True:
                print('find object over .............................................')
                return

            print(names)
            for item in names:
                if item == object:
                    CRUSING_FLOG = False
                    return


def demo_step_find_object(ip,speed=20,dis = 1,object='cup',vAngle =30,hAngle = 90):
    """
    移动，一步一步的寻找物体

     Parameter
     -------
     *ip:string
         -树莓派的
     *object:string
         -要寻找的物体
     *vAngle:int
         -垂直方向的角度
     *hAngle:int
         -水平方向的角度
     *speed:int
         -移动的速度
     *dis:float
         -时间间隔
    """
    #初始化
    car = Car(ip)
    #相机初始化
    camera = Camera()
    camera.connect_server(ip)
    camera.start_receive()
    camera.thread_play()


    ai = Ai()

    car.turn_servo_camera_vertical(vAngle)
    car.turn_servo_camera_horizental(hAngle)

    global STOP_FLAGE
    while True:

        if STOP_FLAGE == True:
            print('over .............................................')
            return

        status=get_status_with_camera(car,camera,ai,object)
        car.turn_servo_camera_horizental(90)
        print(status)
        if status == 'status_move':
            car.run_forward(speed,dis)
        if status == 'status_turn_right':
            car.spin_right(10,0.4)
        if status == 'status_turn_left':
            car.spin_left(10,0.4)
        if status == 'status_stop':
            return

def demo_move_step_find_object(ip,speed=20,dis = 1,object='cup',vAngle =40,hAngle = 80):
    """
    连续移动寻找物体

     Parameter
     -------
     *ip:string
         -树莓派的Ip
     *object:string
         -要寻找的物体
     *vAngle:int
         -垂直方向的角度
     *hAngle:int
         -水平方向的角度
    """
    car = Car(ip)

    camera = Camera()
    camera.connect_server(ip)
    camera.start_receive()
    camera.thread_play()

    ai = Ai()

    car.turn_servo_camera_vertical(vAngle)
    car.turn_servo_camera_horizental(hAngle)

    mainThread_ = threading.Thread(target=find_object,args=(camera,ai,object,))
    mainThread_.start()

    Cruising(car,4)  #以4的速度进行漫游

    car.turn_servo_camera_vertical(vAngle)
    car.turn_servo_camera_horizental(hAngle)

    global STOP_FLAGE
    while True:

        if STOP_FLAGE == True:
            car.stop_all_wheels()
            print('over .............................................')
            return

        status=get_status_with_camera(car,camera,ai,object)
        car.turn_servo_camera_horizental(90)
        print(status)
        if status == 'status_move':
            car.run_forward(speed,dis)
        if status == 'status_turn_right':
            car.spin_right(10,0.4)
        if status == 'status_turn_left':
            car.spin_left(10,0.4)
        if status == 'status_stop':
            return

def get_status_with_camera(car,camera,ai,object):
    """
     根据相机找到物体，分为几种状态

     Parameter
     -------
     *car:class
         -控制车的类
     *camera：class
         -相机类
     *ai:class
         -Ail类
     *object:string
         -寻找的物体
    """
    vTable = [25,45]  #角度 垂直方向
    hTable = [45,90,135] #角度 水平方向
    global STOP_FLAGE
    for pos in vTable:
        car.turn_servo_camera_vertical(pos)
        print('pos:',pos)
        for angle in hTable:

            if STOP_FLAGE == True:
                car.stop_all_wheels()
                print('Cruising over .............................................')
                break

            print('angle:',angle)
            car.turn_servo_camera_horizental(angle)
            time.sleep(2)  #图像稳定时间
            picture = camera.take_picture()
            frame, names, _ = ai.find_object(picture)
            print(names)
            for item in names:
                if item == object:
                    if pos < 40:
                        return 'status_stop'
                    else:
                        if angle == 90:
                            return 'status_move'
                        elif angle < 90:
                            return 'status_turn_right'
                        else:
                            return 'status_turn_left'
    return 'status_move'
def check_object(car,camera,ai,object):
    print('find')
    for item in range(20):
        car.spin_right(4,0.4)
        time.sleep(0.5)
        pic = camera.take_picture()
        ret, names, box = ai.find_object(pic)
        for item in names:
            if item == object:
                return True
    return False


def move_step_find_object_thread(ip,camera,ai,object,vAngle,hAngle):
    car = Car(ip)
    car.turn_servo_camera_vertical(vAngle)
    car.turn_servo_camera_horizental(hAngle)
    global STOP_FLAGE

    while True:
        Cruising(car, 2)  # 以4的速度进行漫游
        if STOP_FLAGE == True:
            car.stop_all_wheels()
            print('find over .............................................')
        car.turn_servo_camera_vertical(vAngle)
        car.turn_servo_camera_horizental(hAngle)
        ret = check_object(car,camera,ai,object)
        if ret:
            break
        mainThread_ = threading.Thread(target=find_object, args=(ip, camera, ai, object,))
        mainThread_.start()

    while True:
        if STOP_FLAGE == True:
            car.stop_all_wheels()
            print('Cruising over .............................................')
            return

        pic = camera.take_picture()
        y = []
        x = []
        x1 = 320
        y1 = 0
        for i in range(1):
            ret, names, box = ai.find_object(pic)
            for item in names:
                if item == object:
                    id = names.index(item)
                    print(box[id])
                    y.append(box[id][1])
                    x.append(box[id][0])
        ysum = 0
        for d in y:
            ysum = ysum + d
        if len(y) > 0:
            y1 = ysum / len(y)
            print(y1)

        xsum = 0
        for d in x:
            xsum = xsum + d
        if len(x) > 0:
            x1 = xsum / len(x)
            print(x1)
        if x1 > 360:
            print('turn right')
            car.turn_right(4, 0.1)

        if x1 < 200:
            print('turn left')
            car.turn_left(4, 0.1)

        if 200 < x1 < 360:
            car.run_forward(4, 0.2)
            if y1 > 400:
                return
        dis =  float(car.distance_from_obstacle())
        if 0 < dis < 20:
            return

def demo_move_step_find_object1(ip,speed=20,dis = 1,object='cup',vAngle =45,hAngle = 80):
    """
    连续移动寻找物体

     Parameter
     -------
     *ip:string
         -树莓派的Ip
     *object:string
         -要寻找的物体
     *vAngle:int
         -垂直方向的角度
     *hAngle:int
         -水平方向的角度
    """
    car = Car(ip)

    camera = Camera()
    camera.connect_server(ip)
    camera.start_receive()

    ai = Ai()

    mainThread_ = threading.Thread(target=find_object,args=(ip,camera,ai,object,))
    mainThread_.start()

    moveThread_ = threading.Thread(target=move_step_find_object_thread,args=(ip, camera, ai, object, vAngle, hAngle,))
    moveThread_.start()

    camera.play()


if __name__ == "__main__":
    start_listenser_thread()
    str = input('输入树莓派的IP:')
    demo_move_step_find_object1(str) #
