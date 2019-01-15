import socket
import _thread
import json
import time
import RPi.GPIO as GPIO
import string
import threading
import RPi.GPIO as GPIO
import socket
import threading


g_dict = {}
g_dict['dir'] = 0

run_car   = '1'  #按键前
back_car  = '2'  #按键后
left_car  = '3'  #按键左
right_car = '4' #按键右
stop_car  = '0'  #按键停

#舵机按键值定义
front_left_servo  = '1'  #前舵机向左
front_right_servo = '2' #前舵机向右
up_servo          = '3'          #摄像头舵机向上
down_servo        = '4'        #摄像头舵机向下
left_servo        = '6'        #摄像头舵机向左
right_servo       = '7'       #摄像头舵机向右
updowninit_servo  = '5'  #摄像头舵机上下复位
stop_servo        = '8'        #舵机停止

#初始化上下左右角度为90度
ServoLeftRightPos = 90
ServoUpDownPos    = 90
g_frontServoPos   = 90
g_nowfrontPos     = 0


#小车电机引脚定义
IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13

#小车按键定义
key = 8

#超声波引脚定义
#超声波引脚定义
EchoPin = 0
TrigPin = 1

#RGB三色灯引脚定义
LED_R = 22
LED_G = 27
LED_B = 24 

#舵机引脚定义
FrontServoPin = 23
ServoUpDownPin = 9
ServoLeftRightPin = 11

#红外避障引脚定义 
AvoidSensorLeft = 12
AvoidSensorRight = 17

#蜂鸣器引脚定义
buzzer = 8

#灭火电机引脚设置
OutfirePin = 2

functionList = {}

#循迹红外引脚定义
#TrackSensorLeftPin1 TrackSensorLeftPin2 TrackSensorRightPin1 TrackSensorRightPin2
#      3                 5                  4                   18
TrackSensorLeftPin1  =  3   #定义左边第一个循迹红外传感器引脚为3口
TrackSensorLeftPin2  =  5   #定义左边第二个循迹红外传感器引脚为5口
TrackSensorRightPin1 =  4   #定义右边第一个循迹红外传感器引脚为4口
TrackSensorRightPin2 =  18  #定义右边第二个循迹红外传感器引脚为18口

#光敏电阻引脚定义
LdrSensorLeft  = 7
LdrSensorRight = 6

#变量的定义
#七彩灯RGB三色变量定义
red   = 0
green = 0
blue  = 0
#TCP通信数据包标志位以及接受和发送数据变量
NewLineReceived = 0
InputString = ''
recvbuf = ''
ReturnTemp = ''
#小车和舵机状态变量
g_CarState = 0
g_ServoState = 0
#小车速度变量
CarSpeedControl = 10 
#寻迹，避障，寻光变量
infrared_track_value = ''
infrared_avoid_value = ''
LDR_value = ''
g_lednum = 0
ServoPin        = 23
servopinUp      = 11
servopincircle  = 9

#设置GPIO口为BCM编码方式
GPIO.setmode(GPIO.BCM)
#忽略警告信息
GPIO.setwarnings(False)

#电机引脚初始化为输出模式
#按键引脚初始化为输入模式
#超声波,RGB三色灯,舵机引脚初始化
#红外避障引脚初始化
def init():
    global pwm_ENA
    global pwm_ENB
    global pwm_servo
    global pwm_FrontServo
    global pwm_UpDownServo
    global pwm_LeftRightServo
    global pwm_rled
    global pwm_gled
    global pwm_servo_circle
    global pwm_servo_up 
    global pwm_bled
    GPIO.setup(EchoPin,GPIO.IN)
    GPIO.setup(TrigPin,GPIO.OUT)   
    GPIO.setup(TrigPin,GPIO.OUT)   
    GPIO.setup(ENA,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(ENB,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(buzzer,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(OutfirePin,GPIO.OUT)
    GPIO.setup(LED_R, GPIO.OUT)
    GPIO.setup(LED_G, GPIO.OUT)
    GPIO.setup(LED_B, GPIO.OUT)
    GPIO.setup(FrontServoPin, GPIO.OUT)
    GPIO.setup(ServoUpDownPin, GPIO.OUT)
    GPIO.setup(ServoLeftRightPin, GPIO.OUT)
    GPIO.setup(AvoidSensorLeft,GPIO.IN)
    GPIO.setup(AvoidSensorRight,GPIO.IN)
    GPIO.setup(LdrSensorLeft,GPIO.IN)
    GPIO.setup(LdrSensorRight,GPIO.IN)
    GPIO.setup(TrackSensorLeftPin1,GPIO.IN)
    GPIO.setup(TrackSensorLeftPin2,GPIO.IN)
    GPIO.setup(TrackSensorRightPin1,GPIO.IN)
    GPIO.setup(TrackSensorRightPin2,GPIO.IN)
    #设置pwm引脚和频率为2000hz
    pwm_ENA = GPIO.PWM(ENA, 2000)
    pwm_ENB = GPIO.PWM(ENB, 2000)
    pwm_ENA.start(0)
    pwm_ENB.start(0)
    #设置舵机的频率和起始占空比
    pwm_FrontServo = GPIO.PWM(FrontServoPin, 50)
    pwm_UpDownServo = GPIO.PWM(ServoUpDownPin, 50)
    pwm_LeftRightServo = GPIO.PWM(ServoLeftRightPin, 50)
    pwm_FrontServo.start(0)
    pwm_UpDownServo.start(0)
    pwm_LeftRightServo.start(0)
    pwm_rled = GPIO.PWM(LED_R, 1000)
    pwm_gled = GPIO.PWM(LED_G, 1000)
    pwm_bled = GPIO.PWM(LED_B, 1000)
    pwm_rled.start(0)
    pwm_gled.start(0)
    pwm_bled.start(0)

    GPIO.setup(EchoPin,GPIO.IN)
    GPIO.setup(TrigPin,GPIO.OUT)
    pwm_servo = GPIO.PWM(ServoPin, 50)
    pwm_servo.start(0)

    GPIO.setup(servopinUp,GPIO.OUT,initial=False)
    GPIO.setup(servopincircle,GPIO.OUT,initial=False)
    pwm_servo_up=GPIO.PWM(servopinUp,50)
    pwm_servo_up.start(0)

    pwm_servo_circle =GPIO.PWM(servopincircle,50)
    pwm_servo_circle.start(0)
    
    
def auto_run(speed, t):
    print('run1')
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
  
    pwm_ENA.ChangeDutyCycle(speed)
    pwm_ENB.ChangeDutyCycle(speed)
    time.sleep(t)


#小车后退
def auto_back(speed, t):
    print('back')
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(speed)
    pwm_ENB.ChangeDutyCycle(speed)
    time.sleep(t)
	
#小车左转	
def auto_left(speed,t):
    print('left1')
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(speed)
    pwm_ENB.ChangeDutyCycle(speed)
    time.sleep(t)

#小车右转
def auto_right(speed,t):
    print('right1')
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(speed)
    pwm_ENB.ChangeDutyCycle(speed)
    time.sleep(t)
    
#小车原地左转
def auto_spin_left(speed, t):
    print('spin left')
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(speed)
    pwm_ENB.ChangeDutyCycle(speed)
    time.sleep(t)

#小车原地右转
def auto_spin_right(speed, t):
    print('spin right....')
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(speed)
    pwm_ENB.ChangeDutyCycle(speed)
    time.sleep(t)
    
#小车停止	
def auto_brake():
   GPIO.output(IN1, GPIO.LOW)
   GPIO.output(IN2, GPIO.LOW)
   GPIO.output(IN3, GPIO.LOW)
   GPIO.output(IN4, GPIO.LOW)


#超声波函数
def Distance_test():
    GPIO.setup(TrigPin,GPIO.OUT) 
    GPIO.output(TrigPin,GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(TrigPin,GPIO.LOW)
    while not GPIO.input(EchoPin):
        pass
    t1 = time.time()
    while GPIO.input(EchoPin):
        pass
    t2 = time.time()
    time.sleep(0.01)
    return ((t2 - t1)* 340 / 2) * 100
	
#舵机旋转到指定角度
def servo_appointed_detection(pos):
    for i in range(18):
        pwm_servo.ChangeDutyCycle(2.5 + 10 * pos/180)
        time.sleep(0.02)
    pwm_servo.ChangeDutyCycle(0)
    time.sleep(0.02)

def servo_appointed_detection_circle(pos):
    for i in range(18):
        pwm_servo_circle.ChangeDutyCycle(2.5 + 10 * pos/180)
        time.sleep(0.02)
    pwm_servo_circle.ChangeDutyCycle(0)
    time.sleep(0.02)


def servo_appointed_detection_up(pos):
    for i in range(18):
        pwm_servo_up.ChangeDutyCycle(2.5 + 10 * pos/180)
        time.sleep(0.02)
    pwm_servo_up.ChangeDutyCycle(0)
    time.sleep(0.02)	

#舵机旋转超声波测距避障，led根据车的状态显示相应的颜色
def servo_color_carstate():
    #开红灯
    GPIO.output(LED_R, GPIO.HIGH)
    GPIO.output(LED_G, GPIO.LOW)
    GPIO.output(LED_B, GPIO.LOW)
    auto_back(20, 20)
    time.sleep(0.08)
    auto_brake()
	
    #舵机旋转到0度，即右侧，测距
    servo_appointed_detection(30)
    time.sleep(0.8)
    rightdistance = Distance_test()
  
    #舵机旋转到180度，即左侧，测距
    servo_appointed_detection(150)
    time.sleep(0.8)
    leftdistance = Distance_test()

    #舵机旋转到90度，即前方，测距
    servo_appointed_detection(80)
    time.sleep(0.8)
    frontdistance = Distance_test()
 
    if leftdistance < 30 and rightdistance < 30 and frontdistance < 30:
        #亮品红色，掉头
        auto_spin_right(85, 85)
        time.sleep(0.58)
    elif leftdistance >= rightdistance:
        auto_spin_left(85,85)
        time.sleep(0.28)
    elif leftdistance <= rightdistance:
        auto_spin_right(85,85)
        time.sleep(0.28)

def AutoRun():
    distance = Distance_test()
    print(distance)
    if distance > 50:
        LeftSensorValue  = GPIO.input(AvoidSensorLeft)
        RightSensorValue = GPIO.input(AvoidSensorRight)

        if LeftSensorValue == True and RightSensorValue == True :
            print(1)
            auto_run(CarSpeedControl,CarSpeedControl)         #当两侧均未检测到障碍物时调用前进函数
        elif LeftSensorValue == True and RightSensorValue == False :
            print(2)
            auto_spin_left(CarSpeedControl, CarSpeedControl)     #右边探测到有障碍物，有信号返回，原地向左转
            time.sleep(0.002)
        elif RightSensorValue == True and LeftSensorValue == False:
            print(3)          
            auto_spin_right(CarSpeedControl, CarSpeedControl)    #左边探测到有障碍物，有信号返回，原地向右转
            time.sleep(0.002)				
        elif RightSensorValue == False and LeftSensorValue == False :
            print(4)              
            auto_spin_right(85, 85)    #当两侧均检测到障碍物时调用固定方向的避障(原地右转)
            time.sleep(0.002)
            auto_run(CarSpeedControl,CarSpeedControl)
            GPIO.output(LED_R, GPIO.LOW)
            GPIO.output(LED_G, GPIO.HIGH)
            GPIO.output(LED_B, GPIO.LOW)
    elif 30<=distance <=50:
        #遇到障碍物,红外避障模块的指示灯亮,端口电平为LOW
        #未遇到障碍物,红外避障模块的指示灯灭,端口电平为HIGH
        LeftSensorValue  = GPIO.input(AvoidSensorLeft)
        RightSensorValue = GPIO.input(AvoidSensorRight)

        if LeftSensorValue == True and RightSensorValue == True :
            auto_run(CarSpeedControl, CarSpeedControl)         #当两侧均未检测到障碍物时调用前进函数
        elif LeftSensorValue == True and RightSensorValue == False :
            auto_spin_left(85, 85)     #右边探测到有障碍物，有信号返回，原地向左转
            time.sleep(0.002)
        elif RightSensorValue == True and LeftSensorValue == False:
            auto_spin_right(85, 85)    #左边探测到有障碍物，有信号返回，原地向右转
            time.sleep(0.002)				
        elif RightSensorValue == False and LeftSensorValue == False :
            auto_spin_right(85, 85)    #当两侧均检测到障碍物时调用固定方向的避障(原地右转)
            time.sleep(0.002)
            auto_run(20, 20)
    elif distance <30:
          servo_color_carstate()
          
def FindObject():
    distance = Distance_test()
    print(distance)
    if distance > 50:
        LeftSensorValue  = GPIO.input(AvoidSensorLeft)
        RightSensorValue = GPIO.input(AvoidSensorRight)

        if LeftSensorValue == True and RightSensorValue == True :
            print(1)
            auto_run(CarSpeedControl,CarSpeedControl)         #当两侧均未检测到障碍物时调用前进函数
        elif LeftSensorValue == True and RightSensorValue == False :
            print(2)
            auto_spin_left(CarSpeedControl, CarSpeedControl)     #右边探测到有障碍物，有信号返回，原地向左转
            time.sleep(0.002)
        elif RightSensorValue == True and LeftSensorValue == False:
            print(3)          
            auto_spin_right(CarSpeedControl, CarSpeedControl)    #左边探测到有障碍物，有信号返回，原地向右转
            time.sleep(0.002)				
        elif RightSensorValue == False and LeftSensorValue == False :
            print(4)              
            auto_spin_right(85, 85)    #当两侧均检测到障碍物时调用固定方向的避障(原地右转)
            time.sleep(0.002)
            auto_run(CarSpeedControl,CarSpeedControl)
            GPIO.output(LED_R, GPIO.LOW)
            GPIO.output(LED_G, GPIO.HIGH)
            GPIO.output(LED_B, GPIO.LOW)
    elif 30<=distance <=50:
        #遇到障碍物,红外避障模块的指示灯亮,端口电平为LOW
        #未遇到障碍物,红外避障模块的指示灯灭,端口电平为HIGH
        LeftSensorValue  = GPIO.input(AvoidSensorLeft)
        RightSensorValue = GPIO.input(AvoidSensorRight)

        if LeftSensorValue == True and RightSensorValue == True :
            auto_run(CarSpeedControl, CarSpeedControl)         #当两侧均未检测到障碍物时调用前进函数
        elif LeftSensorValue == True and RightSensorValue == False :
            auto_spin_left(85, 85)     #右边探测到有障碍物，有信号返回，原地向左转
            time.sleep(0.002)
        elif RightSensorValue == True and LeftSensorValue == False:
            auto_spin_right(85, 85)    #左边探测到有障碍物，有信号返回，原地向右转
            time.sleep(0.002)				
        elif RightSensorValue == False and LeftSensorValue == False :
            auto_spin_right(85, 85)    #当两侧均检测到障碍物时调用固定方向的避障(原地右转)
            time.sleep(0.002)
            auto_run(20, 20)
    elif distance <30:
          servo_color_carstate()   
	
#小车前进	CarSpeedControl
def run():
    print('run')
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(CarSpeedControl)
    pwm_ENB.ChangeDutyCycle(CarSpeedControl)

#小车后退
def back():
    print('back')
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(CarSpeedControl)
    pwm_ENB.ChangeDutyCycle(CarSpeedControl)
	
#小车左转	
def left():
    print('left')
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(CarSpeedControl)
    pwm_ENB.ChangeDutyCycle(CarSpeedControl)

#小车右转
def right():
    print('right')
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(CarSpeedControl)
    pwm_ENB.ChangeDutyCycle(CarSpeedControl)
	
#小车原地左转
def spin_left():
    print('spin_left()')
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(CarSpeedControl)
    pwm_ENB.ChangeDutyCycle(CarSpeedControl)

#小车原地右转
def spin_right():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(CarSpeedControl)
    pwm_ENB.ChangeDutyCycle(CarSpeedControl)

#小车停止	
def stop():
   GPIO.output(IN1, GPIO.LOW)
   GPIO.output(IN2, GPIO.LOW)
   GPIO.output(IN3, GPIO.LOW)

       

def wait():
    print('sleep')
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    time.sleep(1)

				
 
def hand(x):
    swicher={
        0:wait,
        1:run,
        2:left,
        3:right,
        4:back,
        5:spin_left,
        6:spin_right,
        7:stop,
        8:AutoRun,
        9:FindObject
        }
    func=swicher.get(x,None)
    return func()


def moveFunction(func):
    print(type(func))
    for item in func:
        for key in item:
           para = item[key]
           l    =  len(para)
           if l == 1:
              functionList[key](para[0])
           if l == 2:
              functionList[key](para[0],para[1])               
    auto_brake()    
    
    

    #舵机状态判断并执行相应的函数

def netFunction(functionList):
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    
    addr_port = ('172.16.10.227',12347)
    server.bind(addr_port)
    server.listen(1)
    while True:
        time.sleep(0.5)
        conn,addr = server.accept()
        print('start a connect')
        while True:
            try:
                data     =  conn.recv(1024).decode('utf-8')
                print((data))       
                strJson = eval(data)
                
                conn.send(bytes('res ok',encoding='utf8'))   

                print(type(strJson))
                
                process = strJson['function']
                moveThread = threading.Thread(None, target=moveFunction, args=(process,))
                moveThread.start()
            except:
                print('close connect')
                conn.close()
                break
  
        
 
    

def startMoveSever():
       functionList['auto_back']       = auto_back
       functionList['auto_run']        = auto_run
       functionList['auto_left']       = auto_left
       functionList['auto_right']      = auto_right
       functionList['auto_spin_left']  = auto_spin_left
       functionList['auto_spin_right'] = auto_spin_right
       functionList['auto_right']  = auto_right
       functionList['auto_right']  = auto_right
       functionList['servo_appointed_detection']  = servo_appointed_detection 
       functionList['servo_appointed_detection_up']  = servo_appointed_detection_up
       functionList['servo_appointed_detection_circle']  = servo_appointed_detection_circle
       
       init()
       serverThread = threading.Thread(None, target=netFunction, args=(functionList,))
       serverThread.start()

startMoveSever()

      


  
  




