from carLib.thinkland_rpi_camera_client import Camera
from carLib.thinkland_rpi_car_client import Car
from aiLib.thinkland_rpi_ai import  Ai
import random
import threading
import time
import cv2
from aiLib.thinkland_rpi_speaker import Speaker

CRUSING_FLOG  = True

def Cruising(car,speed=4):
    """
    Demonstrates a cruising car that avoids obstacles in a room

    * Use infrared sensors and ultrasonic sensor to gauge obstacles
    * Use LED lights to indicate running/turning decisions
    """
    global CRUSING_FLOG

    try:
        while True:
            if CRUSING_FLOG == False:
                car.stop_all_wheels()
                print('gave over .............................................')
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

def find_object(camera,ai,object):
    global CRUSING_FLOG

    while True:
        pic = camera.take_picture()
        ret, names, _ = ai.find_object(pic)

        print(names)
        for item in names:
            if item == object:
                CRUSING_FLOG = False
                return

def demo_move_find_object(ip,object,vAngle =30,hAngle = 90):
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

    mainThread_ = threading.Thread(target=find_object,args=(camera,ai,object,))
    mainThread_.start()

    Cruising(car,4)  #以4的速度进行漫游

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
    相机初始化
    camera = Camera()
    camera.connect_server(ip)
    camera.start_receive()
    camera.thread_play()

    speaker = Speaker()

    ai = Ai(classes="./aiLib/coco/coco.names", config="./aiLib/coco/yolov3.cfg",
                 weight="./aiLib/coco/yolov3.weights")

    car.turn_servo_camera_vertical(vAngle)
    car.turn_servo_camera_horizental(hAngle)

    while True:
        status=get_status_with_camera(car,camera,ai,object)
        car.turn_servo_camera_horizental(90)
        print(status)
        if status == 'status_move':
            car.run_forward(speed,dis)
        if status == 'status_turn_right':
            car.spin_right(10,0.2)
        if status == 'status_turn_right':
            car.spin_right(10,0.2)
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
    for pos in vTable:
        car.turn_servo_camera_vertical(pos)
        print('pos:',pos)
        for angle in hTable:
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



if __name__ == "__main__":
    demo_step_find_object("172.16.10.227") #
