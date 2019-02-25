import socket
import json
import time

__authors__ = 'xiao long & xu lao shi'
__version__ = 'version 0.02'
__license__ = 'Copyright...'

##############################

class carControl:
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

    def __init__(self):
        self.ip_port  = ('172.16.10.227', 12347)
        self.jsonData = '{"dir":1,"speed":0,"servo":0}';
        self.jsonText = json.loads(self.jsonData)
        self.s        = socket.socket()
        self.order    = {}
        # 建立连接

        self.Dic_Para = {}

    def connect(self,port):
        self.port = port
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
        self.Dic_Para["mode"]            = carControl.THREAD_CALL
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
        self.Dic_Para["mode"]               = carControl.THREAD_CALL
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
            self.Dic_Para["mode"]           = carControl.THREAD_CALL
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
            self.Dic_Para["mode"]           = carControl.THREAD_CALL
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
            self.Dic_Para["mode"]           = carControl.THREAD_CALL
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
            Func_Para["close_led"]          = [carControl.LED_R]
            self.Dic_Para["function"]       = Func_Para
            self.Dic_Para["mode"]           = carControl.THREAD_CALL
            self.__send_order(self.Dic_Para)

            Func_Para                       = {}
            Func_Para["close_led"]          = [carControl.LED_G]
            self.Dic_Para["function"]       = Func_Para
            self.Dic_Para["mode"]           = carControl.THREAD_CALL
            self.__send_order(self.Dic_Para)

            Func_Para                       = {}
            Func_Para["close_led"]          = carControl.LED_B]
            self.Dic_Para["function"]       = Func_Para
            self.Dic_Para["mode"]           = carControl.THREAD_CALL
            self.__send_order(self.Dic_Para)
#########################################################################小车速度控制
    def stop_all_wheels(self, delay = 0):
        """
        Stop wheel movement
        """
        Func_Para = {}
        Func_Para["stop_all_wheels"] = [delay]
        self.Dic_Para["function"]    = Func_Para
        self.Dic_Para["mode"]        = carControl.DERECT_CALL
        self.__send_order(self.Dic_Para)

    def stop_completely(self,delay = 0):
        """
        Completely stop the Car
        """
        Func_Para = {}
        Func_Para["stop_completely"] = [delay]
        self.Dic_Para["function"]    = Func_Para
        self.Dic_Para["mode"]        = carControl.DERECT_CALL
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
        self.Dic_Para["mode"]        = carControl.DERECT_CALL
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
        self.Dic_Para["mode"]        = carControl.DERECT_CALL
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
        self.Dic_Para["mode"]        = carControl.DERECT_CALL
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
        self.Dic_Para["mode"]        = carControl.DERECT_CALL
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
        self.Dic_Para["mode"]        = carControl.DERECT_CALL
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
        self.Dic_Para["mode"]        = carControl.DERECT_CALL
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
        self.Dic_Para["mode"]               = carControl.RETURN_CALL
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
        self.Dic_Para["mode"]                        = carControl.RETURN_CALL
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
        self.Dic_Para["mode"]                         = carControl.RETURN_CALL
        dis = self.__send_order(self.Dic_Para)
        return dis

    @staticmethod
    def demo_ranging():
        """
        例子：超声波测距
        :return:None
        """
        test = carControl()
        test.connect(('172.16.10.227', 12347)) ##需要修改Ip,需要提取指定树莓派的ip

        while True:
            dis = test.distance_from_obstacle()  # 超声波测距
            print(dis)

    @staticmethod
    def demo_run():
        """
        例子：走20秒后停止,然后用卷尺亮出长度，找到当前速度，时间和距离的比值关系
        """
        test = carControl()
        test.connect(('172.16.10.227', 12347)) ##需要修改Ip,需要提取指定树莓派的ip

        while True:
            test.run_forward(10,20)

    @staticmethod
    def demo_run():
        """
        例子：走一个1米的正方形，需要卷尺，量角器，笔等工具
        """
        test = carControl()
        test.connect(('172.16.10.227', 12347)) ##需要修改Ip,需要提取指定树莓派的ip

        while True:
            test.run_forward(10,20)#需要提取保持速度不变，修改时间，然后用卷尺量出其关系
            test.turn_left(4,6)#时间6s，需要修改，看转多少需要
            test.run_forward(10,20)
            test.turn_left(4,6)#时间6s，需要修改，看转多少需要
            test.run_forward(10,20)#需要提取保持速度不变，修改时间，然后用卷尺量出其关系
            test.turn_left(4,6)#时间6s，需要修改，看转多少需要
            test.run_forward(10,20)
            test.turn_left(4,6)#时间6s，需要修改，看转多少需要



################################################################################
"""
超声波的控制
"""
def main():
    carControl.demo_servo_front_roate()

"""
@@@@例子：
#利用库进行简单超声波测距和舵机转动
"""
if __name__ == "__main__":
    mainThread = threading.Thread(target=main)
    mainThread.start()


















