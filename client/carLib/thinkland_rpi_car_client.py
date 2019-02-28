"""
    小车封装类，通过创建Car实例，调用相应的API，可以完成小车的基本控制
    具体控制方法参见本代码中的demo示例
    rpc调用通过zerorpc框架
"""
import time
import random
import zerorpc

__authors__ = 'xiao long & xu lao shi'
__version__ = 'version 0.02'
__license__ = 'Copyright...'


class Car:
    """
    小车类包含以下实例函数：
        * connect                           建立网络连接
        * __send_order                      发送数据流
        * turn_servo_camera_horizental      控制摄像机的舵机进行旋转
        * turn_servo_camera_vertical        控制相机的舵机上升和下降
        * turn_servo_ultrasonic             控制超声波的舵机进行旋转
        * turn_on_led                       开灯
        * turn_off_led                      关灯
        * turn_off_all_led                  关闭所有的灯
        * stop_all_wheels                   停止运动
        * stop_completely                   停止运动 并关闭使能
        * run_forward                       控制车向前进
        * run_reverse                       控制车倒转
        * turn_left                         控制车左转
        * turn_right                        控制车右转
        * spin_left                         控制车左拐弯
        * spin_right                        控制车右拐弯
        * distance_from_obstacle            超声波测距
        * check_left_obstacle_with_sensor   左红外对管检测障碍物是否存在
        * check_right_obstacle_with_sensor  右红外对管检测障碍物是否存在
    """

    DIRECT_CALL = 1         # 直接调用，没有返回参数
    THREAD_CALL = 0
    RETURN_CALL = 2         # 回调，有返回参数

    LED_R = 0               # LED灯的红色单元
    LED_G = 1               # LED灯的绿色单元
    LED_B = 2               # LED灯的蓝色单元

    HAVE_OBSTACLE = 0       # 检测到障碍物
    NO_OBSTACLE = 1         # 没有检测到障碍物

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

    def __init__(self, ip, port=12347):

        self.rpc = zerorpc.Client()
        self.rpc.connect('tcp://{}:{}'.format(ip, port))

    def turn_servo_camera_horizental(self, degree=90):
        """控制摄像头的舵机进行水平方向旋转

        Parameters
        ---------------------------
        * degree：int 类型. 舵机的旋转角度
            - 角度范围: 0-180度，90对应舵机正中间
            - 提示：angle设置角度太小，可能观察不到舵机移动

        Returns
        -------
        * None
        """

        self.rpc.servo_camera_rotate(degree)

    def turn_servo_camera_vertical(self, degree=90):
        """控制摄像头舵机进行垂直方向旋转

        Parameters
        ----------------
        * degree：int . 舵机的旋转角度
            - degree角度范围: 0-180度，90对应舵机正中间
            - 提示：angle设置角度太小，可能观察不到舵机移动

        Returns
        -------
        * None
        """

        self.rpc.servo_camera_rise_fall(degree)

    def turn_servo_ultrasonic(self, degree=90):
        """控制超声波的舵机进行水平方向旋转

        Parameters
        ----------
        * degree：int 类型. 舵机的旋转角度
            - degree角度范围: 0-180度，90对应舵机正中间
            - 提示：angle设置角度太小，可能观察不到舵机移动

        Returns
        -------
        * None
        """

        self.rpc.servo_front_rotate(degree)

    def turn_on_led(self, led):
        """开启LED灯

        Parameters
        -----------
        * led : int
            - LED_R  LED_G  LED_B 三个可选项

        Returns
        -------
        * None
        """

        self.rpc.turn_on_led(led)

    def turn_off_led(self, led):
        """关闭LED灯

        Parameters
        --------------
        * led : int
            - LED_R  LED_G  LED_B 三个可选项

        Returns
        -------
        * None
        """

        self.rpc.turn_off_led(led)

    def turn_off_all_led(self):
        """关闭所有的LED灯
        """
        self.turn_off_led(Car.LED_R)
        self.turn_off_led(Car.LED_G)
        self.turn_off_led(Car.LED_B)

    def stop_all_wheels(self, delay=0):
        """停止小车移动

        Parameters
        ------------
        * delay：int。
            - 延时长度

        Returns
        -------
        * None
        """

        self.rpc.stop_all_wheels(delay)

    def stop_completely(self, delay=0):
        """完全停止小车

        Parameters
        ----------
        * delay：int。
            - 延时长度

        Returns
        -------
        * None
        """

        self.rpc.stop_completely(delay)

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

        self.rpc(speed, duration)

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

        self.rpc.run_reverse(speed, duration)

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

        self.rpc.turn_left(speed, duration)

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

        self.rpc.turn_right(speed, duration)

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


        self.rpc.spin_left(speed, duration)

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
        self.rpc.spin_right(speed, duration)

    def distance_from_obstacle(self):
        """
        Measure the distance between ultrasonic sensor and the obstacle
        that it faces.

        The obstacle should have a relatively smooth surface for this
        to be effective. Distance to fabric or other sound-absorbing
        surfaces is difficult to measure.

        Parameters
        --------------
        * val: int
            - XXXXX

        Returns
        -------
        * int
            - Measured in centimeters: valid range is 2cm to 400cm
        """

        return self.rpc.distance_from_obstacle()

    def check_left_obstacle_with_sensor(self):
        """通过传感器检测小车的左侧是否存在障碍物

        Parameters
        ----------
        * none

        Returns
        -------
        * int
            - 1 : 有障碍
            - 0 : 无障碍
        """

        return self.rpc.check_left_obstacle_with_sensor()

    def check_right_obstacle_with_sensor(self):
        """通过传感器检测小车的右侧是否存在障碍物

        Parameters
        ----------
        * none

        Returns
        -------
        * int
            - 1 : 有障碍
            - 0 : 无障碍
        """

        return self.rpc.check_right_obstacle_with_sensor()


    def obstacle_status_from_infrared(self):
        """
        Return obstacle status obtained by infrared sensors that
        are situated at the left front and right front of the Car.
        The infrared sensors are located on the lower deck, so they
        have a lower view than the ultrasonic sensor.
    
        Indicates blockage by obstacle < 20cm away.
        Depending on sensitivity of sensors, the distance of obstacles
        sometimes needs to be as short as 15cm for effective detection

        Parameters
        ------------
        * num: int
            -
        
        Returns
        -------
        * str
            - one of ['only_left_blocked', 'only_right_blocked',
                    'blocked', 'clear']
        """
        return self.rpc.obstacle_status_from_infrared()

    def line_tracking_turn_type(self):
        """
            Indicates the type of turn required given current sensor values

            Parameters
            ------------

            Returns
            -------
            * str
                - one of ['sharp_left_turn', 'sharp_right_turn',
                          'regular_left_turn', 'regular_right_turn',
                          'smooth_left', 'smooth_right',
                          'straight', 'no_line']
        """

        return self.rpc.line_tracking_turn_type()

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

        self.rpc.turn_servo_ultrasonic(dir,degree)

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

        self.rpc.led_light(color)

    @staticmethod
    def demo_cruising():
        """
        Demonstrates a cruising car that avoids obstacles in a room

        * Use infrared sensors and ultrasonic sensor to gauge obstacles
        * Use LED lights to indicate running/turning decisions
        """
        ip = input("请输入树莓的IP:")
        car = Car(ip)
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

    @staticmethod
    def demo_line_tracking(speed=50):
        """
        Demonstrates the line tracking mode using the line tracking sensor
        """
        ip = input("请输入树莓的IP:")
        car = Car(ip)
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

    @staticmethod
    def demo_led_switch():
        """控制灯demo
        """
        ip = input("请输入树莓的IP:")
        car = Car(ip)
        car.turn_on_led(Car.LED_B)
        time.sleep(2)
        car.turn_on_led(Car.LED_G)
        time.sleep(2)
        car.turn_on_led(Car.LED_R)

    @staticmethod  #
    def demo_car_moving():
        """小车的移动demo
        """
        ip = input("请输入树莓的IP:")
        car = Car(ip)
        run_type = int(input("输入运动类型(0:直线，1：来回，2：转弯，3：拐弯，4：正方形)："))
        if run_type == Car.LINE_MOVE_TYPE:                  # 直线移动
            car.run_forward(5, 2)
        elif run_type == Car.LINE_BACK_FORTH_MOVE_TYPE:     # 来回移动
            car.run_forward(5, 2)
            car.run_reverse(5, 2)
        elif run_type == Car.TURN_CORNER_MOVE_TYPE:         # 转弯
            car.run_forward(5, 2)
            car.turn_left(3, 4)
            car.run_forward(5, 2)
        elif run_type == Car.SPRIN_MOVE_TYPE:               # 拐弯
            car.run_forward(5, 2)
            car.spin_left(3, 2)
            car.run_forward(5, 2)
        elif run_type == Car.RECT_MOVE_TYPE:                # 按正方形路线行驶
            car.run_forward(10, 5)
            car.turn_left(4, 1)
            car.run_forward(10, 5)
            car.turn_left(4, 1)
            car.run_forward(10, 5)
            car.turn_left(4, 1)
            car.run_forward(10, 5)
            car.turn_left(4, 1)

    @staticmethod
    def demo_sensor():
        """传感器控制demo

        """
        ####################################
        # 红外线传感器测试方法：
        #   用手来回挡住传感器，观看传感器的读数变化（在使用传感器前，面向传感器，
        #   调节传感器的旋钮，让右侧的两个灯恰好亮）。当传感器被挡住的时候，左侧的传感器就会亮
        #   根据传感器遇到障碍物类型可以分为下面四种类型：
        #       one of ['only_left_blocked', 'only_right_blocked','blocked', 'clear']

        # 黑白色检测传感器测试方法：
        #   工具：黑色的电工胶布一圈
        #   使用过程：把电工胶布贴在A4纸张上或桌子上，让后把黑白传感器在黑色电工胶布上来回移动，
        #   观看传感器上灯的亮度变化或输出值的变化
        #   当遇到黑色就会变亮，根据它可以做一个巡线机器人。

        # 超声波传感器测试方法
        #   超声波测距：用双手挡住超声波、并做靠近超声波、远离超声波，来回运动，观看超声波读取值的变化
        ########################################

        ip = input("请输入树莓的IP:")
        car = Car(ip)

        sensor_type = int(input("测试传感器类型 0:红外；1:黑白；2:超声波"))
        if sensor_type == 0:    # 红外对管传感器
            while True:
                status = car.obstacle_status_from_infrared()
                print(status)
        elif sensor_type == 1:  # 黑白色检测传感器的使用
            while True:
                status = car.line_tracking_turn_type()
                print(status)
        elif sensor_type == 2:  # 超声波传感器
            while True:
                dis = car.distance_from_obstacle()  # 固定在一个位置查看其变化
                print(dis)


def main():
    demo_index = int(input("请选择演示demo（0：灯光、1：运动、2：传感器、3：漫游、4:巡线）："))
    if demo_index == 0:
        Car.demo_led_switch()          # 灯光操作例子
    elif demo_index == 1:
        Car.demo_car_moving()          # 小车运动操作例子
    elif demo_index == 2:
        Car.demo_sensor()              # 传感器操作例子
    elif demo_index == 3:
        Car.demo_cruising()            # 利用红外传感器、超声波和小车运动组合做漫游服务例子
    elif demo_index == 4:
        Car.demo_line_tracking()       # 利用黑白传感器和小车运动做巡线服务的例子


if __name__ == "__main__":
    main()
