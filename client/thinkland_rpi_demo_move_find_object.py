import platform
type = platform.platform()
print(type)
if 'Mac' in type:
    from client.carLib.thinkland_rpi_camera_client import Camera
    from client.carLib.thinkland_rpi_car_client import Car
    from client.aiLib.thinkland_rpi_ai import Ai
else:
    from carLib.thinkland_rpi_camera_client import Camera
    from carLib.thinkland_rpi_car_client import Car
    from aiLib.thinkland_rpi_ai import Ai

import random
import time
import cv2

from pynput import keyboard
from pynput.keyboard import Key
import threading

"""
停止按钮
"""
STOP_FLAGE = False  # 遇到特殊按钮，则停止demo演示
CAMERA_FLAGE = True


def on_press(key):
    global STOP_FLAGE
    try:
        common = ('alphanumeric key  {0} pressed'.format(key.char))
    except AttributeError:
        if key == Key.caps_lock:
            print('stop demo'.format(
                key))
            STOP_FLAGE = True  # 遇到特殊按钮，则停止demo演示


def listenser():
    with keyboard.Listener(
            on_press=on_press) as listener:
        listener.join()


def start_listenser_thread():
    threadId = threading.Thread(target=listenser)
    threadId.start()


CRUSING_FLOG = True


def Cruising(car, speed=4):
    """
    Demonstrates a cruising car that avoids obstacles in a room

    * Use infrared sensors and ultrasonic sensor to gauge obstacles
    * Use LED lights to indicate running/turning decisions
    """
    global CRUSING_FLOG
    global STOP_FLAGE
    h_angle = [40,  90,  140]  # 角度越多越平滑
    i = 0
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
            car.turn_servo_camera_horizental(h_angle[i])

            i += 1
            if i == len(h_angle):
                i = 0

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
                car.run_reverse(speed, duration=0.1)
                if obstacle_status_from_infrared == 'only_right_blocked':
                    car.spin_left(1.5* speed, duration=random.uniform(0.25, 1.2))
                elif obstacle_status_from_infrared == 'only_left_blocked':
                    car.spin_right(1.5* speed, duration=random.uniform(0.25, 1.2))
                else:
                    car.spin_right(1.5* speed, duration=random.uniform(0.25, 1.2))
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        car.stop_all_wheels()


def find_object(camera, ai, object):
    global CRUSING_FLOG
    global STOP_FLAGE
    while True:
        pic = camera.take_picture()
        ret, names, _ = ai.find_object(pic)

        if STOP_FLAGE == True:
            print('find object over .............................................')
            break

        if 'cup' in names and CRUSING_FLOG is True:
            print("find a cup")
            CRUSING_FLOG = False
            return


def demo_move_find_object(ip, object, vAngle=30, hAngle=90):
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

    ai = Ai(classes="./aiLib/coco/coco.names", config="./aiLib/coco/yolov3.cfg",
            weight="./aiLib/coco/yolov3.weights")

    car.turn_servo_camera_vertical(vAngle)
    car.turn_servo_camera_horizental(hAngle)

    mainThread_ = threading.Thread(target=find_object, args=(camera, ai, object,))
    mainThread_.start()

    Cruising(car, 6)  # 以4的速度进行漫游


def demo_step_find_object(ip, speed=20, dis=1, object='cup', vAngle=30, hAngle=90):
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
    # 初始化
    car = Car(ip)
    # 相机初始化
    camera = Camera()
    camera.connect_server(ip)
    camera.start_receive()
    camera.thread_play()

    ai = Ai(classes="./aiLib/coco/coco.names", config="./aiLib/coco/yolov3.cfg",
            weight="./aiLib/coco/yolov3.weights")

    car.turn_servo_camera_vertical(vAngle)
    car.turn_servo_camera_horizental(hAngle)

    global STOP_FLAGE
    while True:

        if STOP_FLAGE is True:
            print('over .............................................')
            return

        status = get_status_with_camera(car, camera, ai, object)
        car.turn_servo_camera_horizental(90)
        print(status)
        if status == 'status_move':
            car.run_forward(speed, dis)
        if status == 'status_turn_right':
            car.spin_right(10, 0.4)
        if status == 'status_turn_left':
            car.spin_left(10, 0.4)
        if status == 'status_stop':
            return


def demo_move_step_find_object(ip, speed=20, dis=1, object='cup', vAngle=40, hAngle=80):
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

    ai = Ai(classes="./aiLib/coco/coco.names", config="./aiLib/coco/yolov3.cfg",
            weight="./aiLib/coco/yolov3.weights")

    car.turn_servo_camera_vertical(vAngle)
    car.turn_servo_camera_horizental(hAngle)

    mainThread_ = threading.Thread(target=find_object, args=(camera, ai, object,))
    mainThread_.start()

    Cruising(car, 4)  # 以4的速度进行漫游

    car.turn_servo_camera_vertical(vAngle)
    car.turn_servo_camera_horizental(hAngle)

    global STOP_FLAGE
    while CAMERA_FLAGE:

        if STOP_FLAGE == True:
            car.stop_all_wheels()
            print('over .............................................')
            return

        status = get_status_with_camera(car, camera, ai, object)
        car.turn_servo_camera_horizental(90)
        print(status)
        if status == 'status_move':
            car.run_forward(speed, dis)
        if status == 'status_turn_right':
            car.spin_right(10, 0.4)
        if status == 'status_turn_left':
            car.spin_left(10, 0.4)
        if status == 'status_stop':
            return


def get_status_with_camera(car, camera, ai, object):
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
    vTable = [25, 45]  # 角度 垂直方向
    hTable = [45, 90, 135]  # 角度 水平方向
    global STOP_FLAGE
    for pos in vTable:
        car.turn_servo_camera_vertical(pos)
        print('pos:', pos)
        for angle in hTable:

            if STOP_FLAGE == True:
                car.stop_all_wheels()
                print('Cruising over .............................................')
                break

            print('angle:', angle)
            car.turn_servo_camera_horizental(angle)
            time.sleep(2)  # 图像稳定时间
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

def check_object(ai,pic,object):
    """
    在图片中确认是否存在有目标存在

     Parameter
     -------
     *ai:class
         -图像检测
     *pic：mat
         -图像
     *object:string
         -目标名字
     *object:string

     Return
     ---------
     返回‘find’和‘nothing’两种结果
    """
    ret, names, box = ai.find_object(pic)
    for item in names:
        if item == object:
            return 'find'
    return 'nothing'

def check_object_step(camera,car,ai,object):
    """
    在图片中确认是否存在有目标存在

     Parameter
     -------
     *camera:class
         -相机
     *car：class
         -运动
     *ai:class
         -智能检测
     *object:string
         -目标名

     Return
     ---------
     返回‘find’和‘nothing’两种结果
    """
    start_time = time.time()
    time.sleep(2)

    while True:
        car.spin_left(4, 0.4)  # 转动小车寻找cup
        time.sleep(1)#稳定时间
        pic = camera.take_picture()
        ret = check_object(ai, pic,object)
        if ret == 'find':
            print('find')
            return 'find'
        end_time = time.time()
        if start_time - end_time > 8:  # 如果超过8秒没有发现cup，则继续巡游
            return 'nothing'
    return 'nothing'

def move_step_find_object1_thread(ip, camera, ai, object, vAngle, hAngle):
    """
    小车移动寻找目标
     Parameter
     -------
     *ip:string
         -树莓派的地址
     *camera：class
         -相机控制
     *ai:class
         -人工智能类
     *object:string
         --目标名
     *vAngle:int
         --相机垂直角度
     *hAngle:int
         --相机水平角度
     Return
     ---------
     None
    """
    global CRUSING_FLOG
    global STOP_FLAGE
    global CAMERA_FLAGE
    car = Car(ip)
    car.turn_servo_camera_vertical(vAngle)
    car.turn_servo_camera_horizental(hAngle)#运动到相机指定方向

    while  not STOP_FLAGE:
        Cruising(car, 5)  # 以7的速度进行漫游
        car.turn_servo_camera_vertical(vAngle-2)#抬起相机查看
        car.turn_servo_camera_horizental(hAngle)
        ret = check_object_step(camera,car,ai,object)#旋转小车确认
        if ret == 'find':
            break
        if ret == 'nothing':#没有找到，从新找
            mainThread_ = threading.Thread(target=find_object, args=(camera, ai, object,))
            mainThread_.start()
            CRUSING_FLOG = True

    car.spin_left(2, 0.1)  # 回转，减少误差

    start_sensor_check = False

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

        for i in range(1):#多张图寻找
            ret, names, box = ai.find_object(pic)
            for item in names:
                if item == object:
                    id = names.index(item)
                    print(box[id])
                    y.append(box[id][1])
                    x.append(box[id][0])

        #多张图求平均
        ysum = 0
        for d in y:
            ysum = ysum + d
        if len(y) > 0:
            y1 = ysum / len(y)
            print(y1)

        #多张图，求取x平均
        xsum = 0
        for d in x:
            xsum = xsum + d
        if len(x) > 0:
            x1 = xsum / len(x)
            print(x1)


        if x1 > 360:#右转
            print('turn right')
            car.turn_right(4, 0.1)
        elif x1 < 200:#左转
            print('turn left')
            car.turn_left(4, 0.1)
        else:#直行
            car.run_forward(4, 0.2)
        if y1 > 300:#说明车子靠近目标，启动超声波，相机向下移动一点
            start_sensor_check = True
            car.turn_servo_camera_vertical(vAngle + 2)

        #超声波检查
        dis1 = 1000
        dis2 = 1000
        if start_sensor_check:
            car.turn_servo_ultrasonic_angle(50) #左
            time.sleep(0.2)
            dis1 = car.distance_from_obstacle()
            car.turn_servo_ultrasonic_angle(130) #右
            time.sleep(0.2)
            dis2 = car.distance_from_obstacle()
            car.turn_servo_ultrasonic_angle(90)#中
            time.sleep(0.2)

        dis = car.distance_from_obstacle()
        distance_to_obstacle = min(min(dis1,dis2),dis)#选区最小值

        print("distance",distance_to_obstacle)
        if( 0 < distance_to_obstacle and distance_to_obstacle < 30):#检查范围，满足条件说明，车找到杯子了
            print("find cup")
            return







def demo_move_step_find_object1(ip, speed=20, dis=1, object='cup', vAngle=65, hAngle=90):
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
    camera = Camera()
    camera.connect_server(ip)
    camera.start_receive()


    ai = Ai()

    mainThread_ = threading.Thread(target=find_object, args=(camera, ai, object,))
    mainThread_.start()#启动相机查看功能

    moveThread_ = threading.Thread(target=move_step_find_object1_thread,args=(ip, camera, ai, object, vAngle, hAngle,))
    moveThread_.start()#启动寻物

    camera.play()#图像显示

#########################################################################################
#注意运动类Car,在那个线程启动，就只能在那个线程调用
if __name__ == "__main__":
    start_listenser_thread()
    ip = input('输入树莓派的IP:')
    demo_move_step_find_object1(ip)
