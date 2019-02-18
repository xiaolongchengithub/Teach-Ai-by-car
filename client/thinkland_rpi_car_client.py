import socket
import json
import time

################################宏定义
DERECT_CALL = 1
THREAD_CALL = 0
RETURN_CALL = 2

LED_R       = 0
LED_G       = 1
LED_B       = 2

HAVE_OBSTACLE = 0
NO_OBSTACLE   = 1
##############################

class carControl:
    def __init__(self):
        self.ip_port  = ('172.16.10.227', 12347)
        self.jsonData = '{"dir":1,"speed":0,"servo":0}';
        self.jsonText = json.loads(self.jsonData)
        self.s        = socket.socket()
        self.order    = {}
        # 建立连接

        self.Dic_Para = {}

    def connect(self,port):
        self.s.connect(port) #连接远程


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
        str_ord = str(ord)  #dic转换为string
        self.s.send(bytes(str_ord, encoding='utf-8'))#发送消息

        self.recv_data = self.s.recv(1024)#等待接受
        print(self.recv_data)

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
        self.Dic_Para["mode"]            = THREAD_CALL
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
        self.Dic_Para["mode"]               = THREAD_CALL
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
            self.Dic_Para["mode"]           = THREAD_CALL
            self.__send_order(self.Dic_Para)
########################################################################################车灯控制
    def open_led(self,  led):
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
            Func_Para["open_led"]           = [led]
            self.Dic_Para["function"]       = Func_Para
            self.Dic_Para["mode"]           = THREAD_CALL
            self.__send_order(self.Dic_Para)

    def close_led(self,  led):
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
            Func_Para["close_led"]          = [led]
            self.Dic_Para["function"]       = Func_Para
            self.Dic_Para["mode"]           = THREAD_CALL
            self.__send_order(self.Dic_Para)
#########################################################################小车速度控制
    def stop_all_wheels(self, delay = 0):
        """
        Stop wheel movement
        """
        Func_Para = {}
        Func_Para["stop_all_wheels"] = [delay]
        self.Dic_Para["function"]    = Func_Para
        self.Dic_Para["mode"]        = DERECT_CALL
        self.__send_order(self.Dic_Para)

    def stop_completely(self,delay = 0):
        """
        Completely stop the Car
        """
        Func_Para = {}
        Func_Para["stop_completely"] = [delay]
        self.Dic_Para["function"]    = Func_Para
        self.Dic_Para["mode"]        = DERECT_CALL
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
        self.Dic_Para["mode"]        = DERECT_CALL
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
        self.Dic_Para["mode"]        = DERECT_CALL
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
        self.Dic_Para["mode"]        = DERECT_CALL
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
        self.Dic_Para["mode"]        = DERECT_CALL
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
        self.Dic_Para["mode"]        = DERECT_CALL
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
        self.Dic_Para["mode"]        = DERECT_CALL
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
        self.Dic_Para["mode"]               = RETURN_CALL
        dis = self.__send_order(self.Dic_Para)
        return int(dis)

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
        self.Dic_Para["mode"]                        = RETURN_CALL
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
        self.Dic_Para["mode"]                         = RETURN_CALL
        dis = self.__send_order(self.Dic_Para)
        return dis
################################################################################
# test = carControl()
# test.connect(('172.16.10.227', 12347))
#
# while True:
#     dis = test.check_right_obstacle_with_sensor()
#     print(dis)
# test.servo_front_rotate(20)

















