import socket
import time
import random

__authors__ = 'xiao long & xu lao shi'
__version__ = 'version 0.02'
__license__ = 'Copyright...'

##############################

class Car:
    """
    *在客服端对小车的运动进行了封装 包含一下函数：
    *connect 网络连接
    *__send_order  发送数据流
    *servo_camera_rotate 控制相机的舵机进行旋转
    *servo_camera_rise_fall 控制相机的舵机上升和下降
    *servo_front_rotate  控制超声波的舵机进行旋转
    *turn_on_led 打开灯
    *turn_off_led 关灯
    *close_all_led 关闭所有的灯
    *stop_all_wheels 停止运动
    *stop_completely 停止运动 并关闭使能
    *run_forward 车向前进
    *run_reverse 车倒转
    *turn_left 车左转
    *turn_right 车右转
    *spin_left 车左拐弯
    *spin_right 车右拐弯
    *distance_from_obstacle 超声波测距
    *check_left_obstacle_with_sensor 左红外对管检测障碍物是否存在
    *check_right_obstacle_with_sensor  右红外对管检测障碍物是否存在
    """

    ################################宏定义
    DERECT_CALL = 1
    THREAD_CALL = 0
    RETURN_CALL = 2

    LED_R = 0
    LED_G = 1
    LED_B = 2

    HAVE_OBSTACLE = 0
    NO_OBSTACLE = 1

    OPEN = 1
    CLOSE = 1

    LINE_MOVE_TYPE = 0
    LINE_BACK_FORTH_MOVE_TYPE = 1
    TURN_CORNER_MOVE_TYPE = 2
    SPRIN_MOVE_TYPE = 3
    RECT_MOVE_TYPE = 4

    SENSOR_INFRARED_TYPE = 0
    SENSOR_BLACK_WIGHT_TYPE = 1
    SENSOR_ULTRASONIC_TYPE = 2

    def __init__(self):
        self.s        = socket.socket()
        self.order    = {}
        # 建立连接
        self.Dic_Para = {}

    def connect(self,port):
        self.port = (port, 12347)
        self.s.connect(self.port) #连接远程


    def __send_order(self,ord ={"function":[{"auto_run":[8,1]},{"auto_left":[10,2]},{"auto_right":[10,2]}],"mode":1,"speed":10,"time":10}):
        """
        *function:__send_order
        功能:通过Tcp ip发送消息
        ________
        Parameters
        * ord
        Json格式的字符串，连续dict，一个funciton的对应函数数组列表
        ————
        Returns
        * 返回接受到的消息
        """
        try:
            str_ord = str(ord)  # dic转换为string
            self.s.send(bytes(str_ord, encoding='utf-8'))  # 发送消息

            self.recv_data = self.s.recv(1024)  # 等待接受
            print(self.recv_data)
        except socket.error:
            time.sleep(3)
            self.s.connect(self.port)  # 重新连接
        except:
            print('connect error')
        return self.recv_data

####################################################################舵机控制
    def servo_camera_rotate(self , angle):
        """
        *function:servo_camera_rotate
        功能：摄像头的舵机进行旋转
        ________
        Parameters
        * angle：int 类型
        舵机的旋转角度，它的旋转角度对应0-180。其中90是舵机对应正中间
        angle的范围【20-180】角度太小，不能移动
        ————
        Returns
        -------
        * None
        """
        Func_Para                        = {}
        Func_Para["servo_camera_rotate"] = [angle]
        self.Dic_Para["function"]        = Func_Para
        self.Dic_Para["mode"]            = Car.THREAD_CALL
        self.__send_order(self.Dic_Para)

    def servo_camera_rise_fall(self , angle):
        """
        *function:servo_camera_rise_fall
        功能：摄像头舵机进行抬升
        ________
        Parameters
        * angle：int 类型
        舵机的旋转角度，它的旋转角度对应0-180。其中90是舵机对应正中间
        angle的范围【20-180】角度太小，不能移动
        ————
        Returns
        -------
        * None
        """
        Func_Para                           = {}
        Func_Para["servo_camera_rise_fall"] = [angle]
        self.Dic_Para["function"]           = Func_Para
        self.Dic_Para["mode"]               = Car.THREAD_CALL
        self.__send_order(self.Dic_Para)

    def servo_front_rotate(self, angle):
            """
            *function:servo_front_rotate
            功能：控制超声波的舵机进行旋转
            ________
            Parameters
            * angle：int 类型
            【0-180】，中间位置是90度，0度朝向车右边，180度朝向车左边
            ————
            Returns
            -------
            * None
            """
            Func_Para                       = {}
            Func_Para["servo_front_rotate"] = [angle]
            self.Dic_Para["function"]       = Func_Para
            self.Dic_Para["mode"]           = Car.THREAD_CALL
            self.__send_order(self.Dic_Para)
########################################################################################车灯控制
    def turn_on_led(self,  led):
            """
            *function:open_led
            功能：控制LED灯的开关
            ________
            Parameters
            * led : int
            - LED_R  LED_G  LED_B三个选一个
            ————
            Returns
            -------
            * None
            """
            Func_Para                       = {}
            Func_Para["turn_on_led"]           = [led]
            self.Dic_Para["function"]       = Func_Para
            self.Dic_Para["mode"]           = Car.THREAD_CALL
            self.__send_order(self.Dic_Para)

    def turn_off_led(self,  led):
            """
            *function:close_led
            功能：控制LED灯的开关
            ________
            Parameters
            * led : int
            - LED_R  LED_G  LED_B三个选一个
            ————
            Returns
            -------
            * None
            """
            Func_Para                       = {}
            Func_Para["turn_off_led"]       = [led]
            self.Dic_Para["function"]       = Func_Para
            self.Dic_Para["mode"]           = Car.THREAD_CALL
            self.__send_order(self.Dic_Para)

    def close_all_led(self):
            """
            *function:close_led
            功能：关闭所有的灯
            ________
            Parameters
            * Noe
            ————
            Returns
            -------
            * None
            """
            Func_Para                       = {}
            Func_Para["close_led"]          = [Car.LED_R]
            self.Dic_Para["function"]       = Func_Para
            self.Dic_Para["mode"]           = Car.THREAD_CALL
            self.__send_order(self.Dic_Para)

            Func_Para                       = {}
            Func_Para["close_led"]          = [Car.LED_G]
            self.Dic_Para["function"]       = Func_Para
            self.Dic_Para["mode"]           = Car.THREAD_CALL
            self.__send_order(self.Dic_Para)

            Func_Para                       = {}
            Func_Para["close_led"]          = [Car.LED_B]
            self.Dic_Para["function"]       = Func_Para
            self.Dic_Para["mode"]           = Car.THREAD_CALL
            self.__send_order(self.Dic_Para)
#########################################################################小车速度控制
    def stop_all_wheels(self, delay = 0):
        """
        Stop wheel movement
        """
        Func_Para = {}
        Func_Para["stop_all_wheels"] = [delay]
        self.Dic_Para["function"]    = Func_Para
        self.Dic_Para["mode"]        = Car.DERECT_CALL
        self.__send_order(self.Dic_Para)

    def stop_completely(self,delay = 0):
        """
        Completely stop the Car
        """
        Func_Para = {}
        Func_Para["stop_completely"] = [delay]
        self.Dic_Para["function"]    = Func_Para
        self.Dic_Para["mode"]        = Car.DERECT_CALL
        self.__send_order(self.Dic_Para)


    def run_forward(self, speed=50, duration=0.0):
        """
         Run forward

         Parameters
         ----------
         * speed : int
             - Speed of the motors. Valid range [0, 100]
         * duration : float
             - Duration of the motion.
             (default=0.0 - continue indefinitely until other motions are set)
         """
        Func_Para = {}
        Func_Para["run_forward"] = [speed,duration]
        self.Dic_Para["function"]    = Func_Para
        self.Dic_Para["mode"]        = Car.DERECT_CALL
        self.__send_order(self.Dic_Para)

    def run_reverse(self, speed=10, duration=0.0):
        """
        Run forward

        Parameters
        ----------
        * speed : int
            - Speed of the motors. Valid range [0, 100]
        * duration : float
            - Duration of the motion.
            (default=0.0 - continue indefinitely until other motions are set)

        Raises
        ------
        """
        Func_Para = {}
        Func_Para["run_reverse"] = [speed,duration]
        self.Dic_Para["function"]    = Func_Para
        self.Dic_Para["mode"]        = Car.DERECT_CALL
        self.__send_order(self.Dic_Para)

    def turn_left(self, speed=10, duration=0.0):
        """
        Turn left - only right-hand-side wheels run forward

        Parameters
        ----------
        * speed : int
            - Speed of the motors. Valid range [0, 100]
        * duration : float
            - Duration of the motion.
            (default=0.0 - continue indefinitely until other motions are set)

        Raises
        ------
        """
        Func_Para = {}
        Func_Para["turn_left"] = [speed,duration]
        self.Dic_Para["function"]    = Func_Para
        self.Dic_Para["mode"]        = Car.DERECT_CALL
        self.__send_order(self.Dic_Para)

    def turn_right(self, speed=10, duration=0.0):
        """
        Turn right - only left-hand-side wheels run forward

        Parameters
        ----------
        * speed : int
            - Speed of the motors. Valid range [0, 100]
        * duration : float
            - Duration of the motion.
            (default=0.0 - continue indefinitely until other motions are set)

        Raises
        ------
        """
        Func_Para = {}
        Func_Para["turn_right"] = [speed,duration]
        self.Dic_Para["function"]    = Func_Para
        self.Dic_Para["mode"]        = Car.DERECT_CALL
        self.__send_order(self.Dic_Para)

    def spin_left(self, speed=10, duration=0.0):
        """
        Spin to the left in place

        Parameters
        ----------
        * speed : int
            - Speed of the motors. Valid range [0, 100]
        * duration : float
            - Duration of the motion.
            (default=0.0 - continue indefinitely until other motions are set)

        Raises
        ------
        """
        Func_Para = {}
        Func_Para["spin_left"]       = [speed,duration]
        self.Dic_Para["function"]    = Func_Para
        self.Dic_Para["mode"]        = Car.DERECT_CALL
        self.__send_order(self.Dic_Para)

    def spin_right(self, speed=10, duration=0.0):
        """
        Spin to the left in place

        Parameters
        ----------
        * speed : int
            - Speed of the motors. Valid range [0, 100]
        * duration : float
            - Duration of the motion.
            (default=0.0 - continue indefinitely until other motions are set)

        Raises
        ------
        """
        Func_Para = {}
        Func_Para["spin_right"]      = [speed,duration]
        self.Dic_Para["function"]    = Func_Para
        self.Dic_Para["mode"]        = Car.DERECT_CALL
        self.__send_order(self.Dic_Para)
##############################################################################超声波检测
    def distance_from_obstacle(self ,val = 0):
        """
        Measure the distance between ultrasonic sensor and the obstacle
        that it faces.

        The obstacle should have a relatively smooth surface for this
        to be effective. Distance to fabric or other sound-absorbing
        surfaces is difficult to measure.

        Returns
        -------
        * int
            - Measured in centimeters: valid range is 2cm to 400cm
        """
        Func_Para = {}
        Func_Para["distance_from_obstacle"] = [val]
        self.Dic_Para["function"]           = Func_Para
        self.Dic_Para["mode"]               = Car.RETURN_CALL
        dis = self.__send_order(self.Dic_Para)
        return dis

    def check_left_obstacle_with_sensor(self):
        """
        function:check_left_obstacle_with_sensor
        检测小车的左侧是否存在障碍物

        Parameters
        ----------
        * none

        Returns
        -------
        * bool
            - High : 有障碍
            -Low   : 无障碍
        """
        Func_Para = {}
        Func_Para["check_left_obstacle_with_sensor"] = [0]
        self.Dic_Para["function"]                    = Func_Para
        self.Dic_Para["mode"]                        = Car.RETURN_CALL
        dis = self.__send_order(self.Dic_Para)
        return int(dis)

    def check_right_obstacle_with_sensor(self):
        """
        function:check_right_obstacle_with_sensor
        检测小车的右侧是否存在障碍物

        Parameters
        ----------
        * none
        Returns
        -------
        * bool
            - High : 有障碍
            -Low   : 无障碍
        """
        Func_Para = {}
        Func_Para["check_right_obstacle_with_sensor"] = [0]
        self.Dic_Para["function"]                     = Func_Para
        self.Dic_Para["mode"]                         = Car.RETURN_CALL
        dis = self.__send_order(self.Dic_Para)
        return dis

    def obstacle_status_from_infrared(self,num = 0):
        """
        Return obstacle status obtained by infrared sensors that
        are situated at the left front and right front of the Car.
        The infrared sensors are located on the lower deck, so they
        have a lower view than the ultrasonic sensor.
    
        Indicates blockage by obstacle < 20cm away.
        Depending on sensitivity of sensors, the distance of obstacles
        sometimes needs to be as short as 15cm for effective detection
        
        Returns
        -------
        * str
            - one of ['only_left_blocked', 'only_right_blocked',
                    'blocked', 'clear']
        """
        Func_Para = {}
        Func_Para["obstacle_status_from_infrared"] = [num]
        self.Dic_Para["function"] = Func_Para
        self.Dic_Para["mode"] = Car.RETURN_CALL
        status = self.__send_order(self.Dic_Para)
        return status

    def line_tracking_turn_type(self ,num = 4):
        """
            Indicates the type of turn required given current sensor values

            Returns
            -------
            * str
                - one of ['sharp_left_turn', 'sharp_right_turn',
                          'regular_left_turn', 'regular_right_turn',
                          'smooth_left', 'smooth_right',
                          'straight', 'no_line']
        """
        Func_Para = {}
        Func_Para["line_tracking_turn_type"] = [num]
        self.Dic_Para["function"] = Func_Para
        self.Dic_Para["mode"] = Car.RETURN_CALL
        status = self.__send_order(self.Dic_Para)
        return status

    def turn_servo_ultrasonic(self, dir='degree', degree=90):
        """
        Turn the servo for ultrasonic sensor

        Parameters
        ----------
        * dir : str
            - one of ['left', 'center', 'right']
            - if dir == 'degree', use degree parameter
        * degree : int
            - the angle to turn, measured in degree [0, 180]
            - if dir is specified other than 'degree', this is ignored
        """
        Func_Para = {}
        Func_Para["turn_servo_ultrasonic"] = [dir,degree]
        self.Dic_Para["function"] = Func_Para
        self.Dic_Para["mode"] = Car.DERECT_CALL
        self.__send_order(self.Dic_Para)


    def led_light(self, color):
        """
        Shine LED light

        Parameters
        ----------
        * color : str
            - one of ['red', 'green', 'blue',
                      'yellow', 'cyan', 'purple'
                      'white', 'off']
        """
        Func_Para = {}
        Func_Para["led_light"] = [color]
        self.Dic_Para["function"] = Func_Para
        self.Dic_Para["mode"] = Car.DERECT_CALL
        self.__send_order(self.Dic_Para)


    @staticmethod  #自动巡游功能
    def demo_cruising():
        """
        Demonstrates a cruising car that avoids obstacles in a room

        * Use infrared sensors and ultrasonic sensor to gauge obstacles
        * Use LED lights to indicate running/turning decisions
        """
        car = Car()
        car.connect('172.16.10.227')
        try:
            while True:
                obstacle_status_from_infrared = car.obstacle_status_from_infrared()
                should_turn = True
                if obstacle_status_from_infrared == 'clear':
                    should_turn = False
                    obstacle_status_from_ultrasound = \
                        car.obstacle_status_from_ultrasound()
                    if obstacle_status_from_ultrasound == 'clear':
                        car.run_forward(speed=10)
                    elif obstacle_status_from_ultrasound == 'approaching_obstacle':
                        car.run_forward(speed=5)
                    else:
                        should_turn = True
                if should_turn:
                    car.run_reverse(duration=0.02)
                    if obstacle_status_from_infrared == 'only_right_blocked':
                        car.spin_left(duration=random.uniform(0.25, 1.0))
                    elif obstacle_status_from_infrared == 'only_left_blocked':
                        car.spin_right(duration=random.uniform(0.25, 1.0))
                    else:
                        car.spin_right(duration=random.uniform(0.25, 1.0))
        except KeyboardInterrupt:
            car.stop_completely()

    @staticmethod  #自动巡线功能
    def demo_line_tracking(speed=50):
        """
        Demonstrates the line tracking mode using the line tracking sensor
        """
        time.sleep(2)
        car = Car()
        car.connect('172.16.10.227') #需要根据需求

        try:
            while True:
                turn = car.line_tracking_turn_type()
                if turn == 'straight':
                    car.run_forward(speed=speed)
                elif turn == 'smooth_left':
                    car.turn_left(speed=speed * 0.75)
                elif turn == 'smooth_right':
                    car.turn_right(speed=speed * 0.75)
                elif turn == 'regular_left_turn':
                    car.spin_left(speed=speed * 0.75)
                elif turn == 'regular_right_turn':
                    car.spin_right(speed=speed * 0.75)
                elif turn == 'sharp_left_turn':
                    car.spin_left(speed=speed)
                elif turn == 'sharp_right_turn':
                    car.spin_right(speed=speed)
        except KeyboardInterrupt:
            car.stop_completely()

    @staticmethod  #输出电平，控制小车的灯的颜色
    def demo_light():
        """
        控制灯
        - one of ['red', 'green', 'blue',
          'yellow', 'cyan', 'purple'
          'white', 'off']
        """
        port = input("请输入树莓的IP:")
        car = Car()
        car.connect(port)
        car.led_light('red')

    @staticmethod  #小车的直行、转动、正方形
    def demo_car_run():
        """
        运动类型：0 ：直线运动                LINE_MOVE_TYPE = 0
                  1 ：来回运动                LINE_BACK_FORTH_MOVE_TYPE = 1
                  2 : 转弯                    TURN_CORNER_MOVE_TYPE = 2
                  3 ：拐弯                    SPRIN_MOVE_TYPE = 3
                  4 ：正方形                  RECT_MOVE_TYPE = 4
        """
        run_type = 0
        car = Car()
        port = input("请输入树莓的IP:")
        car.connect(port)

        run_type = int(input("输入运动类型(0:直线，1：来回，2：转弯，3：拐弯，4：正方形)："))
        if run_type == Car.LINE_MOVE_TYPE:
            car.run_forward(5,2) #按照5的速度，走10s
        elif run_type == Car.LINE_BACK_FORTH_MOVE_TYPE:
            car.run_forward(5,2) #按照5的速度，走10s
            car.run_reverse(5,2) #按照5的速度，原路返回走10s
        elif run_type == Car.TURN_CORNER_MOVE_TYPE:
            car.run_forward(5,2) #按照5的速度，走10s
            car.turn_left(3,4)  #转弯
            car.run_forward(5,2) #按照5的速度，走10s
        elif  run_type == Car.SPRIN_MOVE_TYPE:
            car.run_forward(5,2) #按照5的速度，走10s
            car.spin_left(3,2)    #转弯
            car.run_forward(5,2) #按照5的速度，走10s
        elif run_type == Car.RECT_MOVE_TYPE:
            car.run_forward(10,5)#需要提取保持速度不变
            car.turn_left(4,1)#时间6s，需要修改，确保转90度，每一台设备有微小的差异
            car.run_forward(10,5)
            car.turn_left(4,1)#需要修改时间，确保转90度，每一台设备有微小的差异
            car.run_forward(10,5)
            car.turn_left(4,1)#时间6s，需要修改时间，确保转90度，每一台设备有微小的差异
            car.run_forward(10,5)
            car.turn_left(4,1)#时间6s，需要修改，看转多少需要

    @staticmethod  #小车的直行、转动、正方形
    def demo_sensor():
        """
        传感器类型：0 ：红外对管传感器的使用                  SENSOR_INFRARED_TYPE = 0
                   1 ：黑白传感器的使用               SENSOR_BLACK_WIGHT_TYPE = 1
                  2 : 超声波传感器                 SENSOR_ULTRASONIC_TYPE = 2
        """
        sensor_type = 0
        car = Car()
        port = input("请输入树莓的IP:")
        car.connect(port)
        sensor_type = int(input("测试传感器类型 0:红外；1:黑白；2:超声波"))
        if sensor_type == 0:
            """
            #用手来回挡住传感器，观看传感器的读数变化（在使用传感器前，面向传感器，                              
            调节传感器的旋钮，让右侧的两个灯恰好亮）。当传感器被挡住的时候，左侧的传感器就会亮
            根据传感器遇到障碍物类型可以分为下面四种类型
            one of ['only_left_blocked', 'only_right_blocked','blocked', 'clear']
            """
            while True:
                status = car.obstacle_status_from_infrared()
                print(status)
        elif sensor_type == 1:
            """
            #黑色的电工胶布一圈                          
            使用过程：把电工胶布贴在A4纸张上或桌子上，让后把黑白传感器在黑色电工胶布上来回移动，观看传感器上灯的亮度变化或输出值的变化
            当遇到黑色就会变亮，根据它可以做一个巡线机器人。根据四个传感器亮的组合可以分为下面几种情况:
            ['sharp_left_turn', 'sharp_right_turn','regular_left_turn', 'regular_right_turn',
            'smooth_left', 'smooth_right','straight', 'no_line']
            """
            while True:
                status = car.line_tracking_turn_type()
                print(status)
        elif sensor_type == 2:
            """
            #超声波测距：用双手挡住超声波、并做靠近超声波、远离超声波，来回运动，观看超声波读取值的变化
            """
            while True:
                dis = car.distance_from_obstacle()  #固定在一个位置查看其变化
                print(dis)

                # dis = car.servo_front_rotate(30) #旋转超声波，并进行测距
                # print(dis)
                # dis = car.servo_front_rotate(90)
                # print(dis)
                # dis = car.servo_front_rotate(120)
                # print(dis)


learning_level = 0 # 学习等级 0：初级 设置电平，可以控制灯的开和关
                   # 学习等级 1：控制小车直行、运动、左转等
                   # 学习等级 2：控制小车的传感器
                   # 学习等级 3：控制小车漫游
                   # 学习等级 4：控制小车巡线

def main():
    learning_level = int(input("请输入学习等级（0：灯光、1：运动、2：传感器、3：漫游、4:巡线）："))
    print(learning_level)
    if learning_level == 0:
        Car.demo_light()   #灯光操作例子
    elif learning_level == 1:
        Car.demo_car_run() #小车运动操作例子
    elif learning_level == 2:
        Car.demo_sensor()  #传感器操作例子
    elif learning_level == 3:
        Car.demo_cruising()  # 利用红外传感器、超声波和小车运动组合做漫游服务例子
    elif learning_level == 4:
        Car.demo_line_tracking() #利用黑白传感器和小车运动做巡线服务的例子

"""
@@@@例子：
#在树莓派上运行各种例子
"""
if __name__ == "__main__":
    main()


















