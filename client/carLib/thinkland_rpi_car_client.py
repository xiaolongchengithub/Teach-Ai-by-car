"""
    小车封装类，通过创建Car实例，调用相应的API，可以完成小车的基本控制
    具体控制方法参见本代码中的demo示例
    rpc调用通过zerorpc框架
"""
import time
import random
import zerorpc
from pynput import keyboard
import threading

__authors__ = 'xiao long & xu lao shi'
__version__ = 'version 0.02'
__license__ = 'Copyright...'


class KeyboardMixin:
    """按键检测Mixin
        由于macos处于安全考虑，在没有sudo的情况下不能捕获到普通按键
        只能捕获特殊按键，例如:control、caps lock、command、shift等特殊按键
    """

    STOP_DEMO = False

    def on_press(self, key):
        try:
            print('alphanumeric key {0} pressed'.format(
                key.char))
        except AttributeError:
            print('stop demo'.format(
                key))
            self.STOP_DEMO = True  # 遇到特殊按钮，则停止demo演示

    def keyboard_listener(self):
        with keyboard.Listener(
                on_press=self.on_press) as listener:
            listener.join()

    def start_listen_keyboard(self):
        """启动子线程，监听键盘事件
        """
        print("按下control、shit、caps lock 、tab等特殊按键可以停止demo")
        keyboard_thread = threading.Thread(target=self.keyboard_listener)
        keyboard_thread.start()


class DemoMixin:

    def demo_cruising(self):
        """
        Demonstrates a cruising car that avoids obstacles in a room
        * Use infrared sensors and ultrasonic sensor to gauge obstacles
        * Use LED lights to indicate running/turning decisions
        """
        try:
            while True:
                obstacle_status_from_infrared = self.obstacle_status_from_infrared()
                should_turn = True
                if obstacle_status_from_infrared == 'clear':
                    should_turn = False
                    obstacle_status_from_ultrasound = \
                        self.obstacle_status_from_ultrasound()
                    if obstacle_status_from_ultrasound == 'clear':
                        self.run_forward(speed=10)
                    elif obstacle_status_from_ultrasound == 'approaching_obstacle':
                        self.run_forward(speed=5)
                    else:
                        should_turn = True
                if should_turn:
                    self.run_reverse(duration=0.02)
                    if obstacle_status_from_infrared == 'only_right_blocked':
                        self.spin_left(duration=random.uniform(0.25, 1.0))
                    elif obstacle_status_from_infrared == 'only_left_blocked':
                        self.spin_right(duration=random.uniform(0.25, 1.0))
                    else:
                        self.spin_right(duration=random.uniform(0.25, 1.0))
                if self.STOP_DEMO:
                    self.STOP_DEMO = False
                    self.stop_completely()
                    break
        except KeyboardInterrupt:
            self.stop_completely()

    def demo_line_tracking(self):
        """
        Demonstrates the line tracking mode using the line tracking sensor
        """
        try:
            speed = input("请设置小车移动速度(10-50):")
            speed = int(speed)
            while True:

                turn = self.line_tracking_turn_type()
                print(turn)
                if turn == 'straight':
                    self.run_forward(speed=speed)
                elif turn == 'smooth_left':
                    self.turn_left(speed=speed * 0.75)
                elif turn == 'smooth_right':
                    self.turn_right(speed=speed * 0.75)
                elif turn == 'regular_left_turn':
                    self.spin_left(speed=speed * 0.75)
                elif turn == 'regular_right_turn':
                    self.spin_right(speed=speed * 0.75)
                elif turn == 'sharp_left_turn':
                    self.spin_left(speed=speed)
                elif turn == 'sharp_right_turn':
                    self.spin_right(speed=speed)
                if self.STOP_DEMO:
                    self.STOP_DEMO = False
                    self.stop_completely()
                    break
        except KeyboardInterrupt:
            self.stop_completely()

    def demo_led_switch(self):
        """控制灯demo
        """
        self.turn_on_led(Car.LED_B)
        time.sleep(2)
        self.turn_on_led(Car.LED_G)
        time.sleep(2)
        self.turn_on_led(Car.LED_R)

    def demo_car_moving(self):
        """小车的移动demo
        """
        run_type = int(input("输入运动类型(0:直线，1：来回，2：转弯，3：拐弯，4：正方形)："))
        if run_type == Car.LINE_MOVE_TYPE:  # 直线移动
            self.run_forward(5, 2)
        elif run_type == Car.LINE_BACK_FORTH_MOVE_TYPE:  # 来回移动
            self.run_forward(5, 2)
            self.run_reverse(5, 2)
        elif run_type == Car.TURN_CORNER_MOVE_TYPE:  # 转弯
            self.run_forward(5, 2)
            self.turn_left(3, 4)
            self.run_forward(5, 2)
        elif run_type == Car.SPRIN_MOVE_TYPE:  # 拐弯
            self.run_forward(5, 2)
            self.spin_left(3, 2)
            self.run_forward(5, 2)
        elif run_type == Car.RECT_MOVE_TYPE:  # 按正方形路线行驶
            self.run_forward(10, 5)
            self.turn_left(4, 1)
            self.run_forward(10, 5)
            self.turn_left(4, 1)
            self.run_forward(10, 5)
            self.turn_left(4, 1)
            self.run_forward(10, 5)
            self.turn_left(4, 1)

    def demo_sensor(self):
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
        # global STOP_DEMO
        # ip = input("请输入树莓的IP:")
        # ip = "172.16.10.227"
        # car = Car(ip)

        sensor_type = int(input("测试传感器类型 0:红外；1:黑白；2:超声波"))
        while True:
            if sensor_type == 0:
                status = self.obstacle_status_from_infrared()
                print(status)
            elif sensor_type == 1:
                status = self.line_tracking_turn_type()
                print(status)
            elif sensor_type == 2:
                dis = self.distance_from_obstacle()  # 固定在一个位置查看其变化
                print(dis)
            if self.STOP_DEMO:
                self.STOP_DEMO = False
                break

    def start_demo(self):
        while True:
            demo_index = int(input("请选择演示demo（0：灯光、1：运动、2：传感器、3：漫游、4:巡线）："))
            if demo_index == 0:
                self.demo_led_switch()  # 灯光操作例子
            elif demo_index == 1:
                self.demo_car_moving()  # 小车运动操作例子
            elif demo_index == 2:
                self.demo_sensor()  # 传感器操作例子
            elif demo_index == 3:
                self.demo_cruising()  # 利用红外传感器、超声波和小车运动组合做漫游服务例子
            elif demo_index == 4:
                self.demo_line_tracking()  # 利用黑白传感器和小车运动做巡线服务的例子


class Car(KeyboardMixin, DemoMixin):
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

        self.rpc.turn_servo_camera_horizental(degree)


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

        self.rpc.turn_servo_camera_vertical(degree)

    # def turn_servo_ultrasonic(self, degree=90):
    #     """控制超声波的舵机进行水平方向旋转
    #
    #     Parameters
    #     ----------
    #     * degree：int 类型. 舵机的旋转角度
    #         - degree角度范围: 0-180度，90对应舵机正中间
    #         - 提示：angle设置角度太小，可能观察不到舵机移动
    #
    #     Returns
    #     -------
    #     * None
    #     """
    #
    #     self.rpc.servo_front_rotate(degree)

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
        self.led_status = True
        while self.led_status:
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

    def stop_all_wheels(self):
        """停止小车移动
        Parameters
        ------------
        * delay：int。
            - 延时长度
        Returns
        -------
        * None
        """

        self.rpc.stop_all_wheels()

    def stop_completely(self):
        """完全停止小车
        Parameters
        ----------
        * delay：int。
            - 延时长度
        Returns
        -------
        * None
        """

        self.rpc.stop_completely()

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

        self.rpc.run_forward(speed, duration)

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
            (defa17ult=0.0 - continue indefinitely until other motions are set)
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

        self.rpc.turn_servo_ultrasonic(dir, degree)

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

    def obstacle_status_from_ultrasound(self):
        return self.rpc.obstacle_status_from_ultrasound()


def main():
    ip = input("请输入树莓的IP:")
    car = Car(ip)
    car.start_listen_keyboard()
    car.start_demo()


if __name__ == "__main__":
    main()

