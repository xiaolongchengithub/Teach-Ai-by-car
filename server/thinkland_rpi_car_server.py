"""
    小车服务端类，该类提供了供远程控制小车的所有api
    直接运行本文件就会启动rpc服务
"""

import time
import RPi.GPIO as GPIO
import random
import zerorpc

__authors__ = 'xiao long & xu lao shi'
__version__ = 'version 0.01'
__license__ = 'Copyright...'


class Car:
    """小车服务端类
    """

    #  直流电机引脚定义
    PIN_MOTOR_LEFT_FORWARD = 20
    PIN_MOTOR_LEFT_BACKWARD = 21
    PIN_MOTOR_RIGHT_FORWARD = 19
    PIN_MOTOR_RIGHT_BACKWARD = 26
    PIN_MOTOR_LEFT_SPEED = 16
    PIN_MOTOR_RIGHT_SPEED = 13

    # 超声波引脚定义
    PIN_ECHO = 0
    PIN_TRIG = 1

    # 彩色灯引脚定义
    PIN_LED_R = 22
    PIN_LED_G = 27
    PIN_LED_B = 24

    # 伺服电机引脚定义
    PIN_FRONT_SERVER = 23
    PIN_UP_DOWN_SERVER = 11
    PIN_LEFT_RIGHT_SERVER = 9

    # 避障脚定义
    PIN_AVOID_LEFT_SENSOR = 12
    PIN_AVOID_RIGHT_SENSOR = 17

    # 巡线传感器引脚定义
    PIN_TRACK_1 = 3  # counting From left, 1
    PIN_TRACK_2 = 5  # 2
    PIN_TRACK_3 = 4  # 3
    PIN_TRACK_4 = 18  # 4

    # 蜂鸣器
    PIN_BUFFER = 8

    HAVE_OBSTACLE = 0
    NO_OBSTACLE = 1

    SERVO_TOTAL_STEP = 18

    LED_R = 0
    LED_G = 1
    LED_B = 2

    OPEN = GPIO.HIGH
    CLOSE = GPIO.LOW

    LINE_MOVE_TYPE = 0
    LINE_BACK_FORTH_MOVE_TYPE = 1
    TURN_CORNER_MOVE_TYPE = 2
    SPRIN_MOVE_TYPE = 3
    RECT_MOVE_TYPE = 4

    SENSOR_INFRARED_TYPE = 0
    SENSOR_BLACK_WIGHT_TYPE = 1
    SENSOR_ULTRASONIC_TYPE = 2

    Car_Init = False

    def __init__(self):
        GPIO.setmode(GPIO.BCM)  # 设置GPIO口为BCM编码方式
        GPIO.setwarnings(False)  # 忽略警告信息
        self.__init_level()  # 初始化IO
        self.__init_pwm()  # 初始化 pwm

        Car.Car_Init = True
        self.LED_FLAG = {}
        self.LED_FLAG[Car.LED_R] = True
        self.LED_FLAG[Car.LED_G] = True
        self.LED_FLAG[Car.LED_B] = True

    def __init_level(self):
        """初始化小车各部分引脚电平
        设置Io的输出方式：
            输出模式：即是具有上拉电阻
            输入模式：即是能获取电平的高低，在数字电路上高于二极管的导通电压为高，否则为低电平

        """
        # 设置超声波电平
        GPIO.setup(Car.PIN_ECHO, GPIO.IN)
        GPIO.setup(Car.PIN_TRIG, GPIO.OUT)

        # 小车输出电平
        GPIO.setup(Car.PIN_MOTOR_LEFT_FORWARD, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(Car.PIN_MOTOR_LEFT_BACKWARD, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(Car.PIN_MOTOR_RIGHT_FORWARD, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(Car.PIN_MOTOR_RIGHT_BACKWARD, GPIO.OUT, initial=GPIO.LOW)

        # 小车速度
        GPIO.setup(Car.PIN_MOTOR_LEFT_SPEED, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(Car.PIN_MOTOR_RIGHT_SPEED, GPIO.OUT, initial=GPIO.HIGH)

        # 蜂鸣器电平
        GPIO.setup(Car.PIN_BUFFER, GPIO.OUT, initial=GPIO.HIGH)

        # 彩灯输出设置
        GPIO.setup(Car.PIN_LED_R, GPIO.OUT)
        GPIO.setup(Car.PIN_LED_G, GPIO.OUT)
        GPIO.setup(Car.PIN_LED_B, GPIO.OUT)

        # 舵机设置为输出模式
        GPIO.setup(Car.PIN_FRONT_SERVER, GPIO.OUT)
        GPIO.setup(Car.PIN_UP_DOWN_SERVER, GPIO.OUT)
        GPIO.setup(Car.PIN_LEFT_RIGHT_SERVER, GPIO.OUT)

        # 避障传感器设置为输入模式
        GPIO.setup(Car.PIN_AVOID_LEFT_SENSOR, GPIO.IN)
        GPIO.setup(Car.PIN_AVOID_RIGHT_SENSOR, GPIO.IN)

        # 设置寻线传感器电平为输入
        GPIO.setup(Car.PIN_TRACK_1, GPIO.IN)
        GPIO.setup(Car.PIN_TRACK_2, GPIO.IN)
        GPIO.setup(Car.PIN_TRACK_3, GPIO.IN)
        GPIO.setup(Car.PIN_TRACK_4, GPIO.IN)

    def __init_pwm(self):
        """初始化pwm
        设置PWM，是脉冲宽度调制缩写
        它是通过对一系列脉冲的宽度进行调制，等效出所需要的波形（包含形状以及幅值），对模拟信号电平进行数字编码，
        也就是说通过调节占空比的变化来调节信号、能量等的变化，占空比就是指在一个周期内，信号处于高电平的时间占据整个信号周期的百分比
        通过设置占空比来控制车速、舵机的角度、灯光的亮度
        """

        # 初始化控制小车的PWM
        self.__pwm_left_speed = GPIO.PWM(Car.PIN_MOTOR_LEFT_SPEED, 2000)
        self.__pwm_right_speed = GPIO.PWM(Car.PIN_MOTOR_RIGHT_SPEED, 2000)

        self.__pwm_left_speed.start(0)
        self.__pwm_right_speed.start(0)

        # 设置舵机的频率和起始占空比
        self.__pwm_front_servo_pos = GPIO.PWM(Car.PIN_FRONT_SERVER, 50)
        self.__pwm_up_down_servo_pos = GPIO.PWM(Car.PIN_UP_DOWN_SERVER, 50)
        self.__pwm_left_right_servo_pos = GPIO.PWM(Car.PIN_LEFT_RIGHT_SERVER, 50)

        self.__pwm_front_servo_pos.start(0)
        self.__pwm_up_down_servo_pos.start(0)
        self.__pwm_left_right_servo_pos.start(0)

    def __set_motion(self, left_forward, left_backward,
                     right_forward, right_backward,
                     speed_left, speed_right,
                     duration=0.0):
        """
        Helper function to set car wheel motions

        Parameters
        ----------
        * left_forward   : GPIO.HIGH or LOW
        * left_backward  : GPIO.HIGH or LOW
        * right_forward  : GPIO.HIGH or LOW
        * right_backward : GPIO.HIGH or LOW
        * speed_left     : int
            An integer [0,100] for left motors speed
        * speed_right    : int
            An integer [0,100] for right motors speed
        * duration       : float
            Duration of the motion.
            (default=0.0 - continue indefinitely until called again)
        Raises
        ------
        """
        GPIO.output(Car.PIN_MOTOR_LEFT_FORWARD, left_forward)
        GPIO.output(Car.PIN_MOTOR_LEFT_BACKWARD, left_backward)
        GPIO.output(Car.PIN_MOTOR_RIGHT_FORWARD, right_forward)
        GPIO.output(Car.PIN_MOTOR_RIGHT_BACKWARD, right_backward)
        self.__pwm_left_speed.ChangeDutyCycle(speed_left)
        self.__pwm_right_speed.ChangeDutyCycle(speed_right)
        if duration > 0.0:
            time.sleep(duration)
            self.__pwm_left_speed.ChangeDutyCycle(0)
            self.__pwm_right_speed.ChangeDutyCycle(0)

    @staticmethod
    def __led_light(r, g, b):
        """
         __led_light

         Parameters
         ----------
         * r : bool
             - GPIO.HIGH  GPIO.LOW
         * g : bool
             - GPIO.HIGH  GPIO.LOW
         * b : bool
             - GPIO.HIGH  GPIO.LOW
        """
        GPIO.output(Car.PIN_LED_R, r)
        GPIO.output(Car.PIN_LED_G, g)
        GPIO.output(Car.PIN_LED_B, b)

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
        if color == 'red':
            self.__led_light(GPIO.HIGH, GPIO.LOW, GPIO.LOW)
        elif color == 'green':
            self.__led_light(GPIO.LOW, GPIO.HIGH, GPIO.LOW)
        elif color == 'blue':
            self.__led_light(GPIO.LOW, GPIO.LOW, GPIO.HIGH)
        elif color == 'yellow':
            self.__led_light(GPIO.HIGH, GPIO.HIGH, GPIO.LOW)
        elif color == 'cyan':
            self.__led_light(GPIO.LOW, GPIO.HIGH, GPIO.HIGH)
        elif color == 'purple':
            self.__led_light(GPIO.HIGH, GPIO.LOW, GPIO.HIGH)
        elif color == 'white':
            self.__led_light(GPIO.HIGH, GPIO.HIGH, GPIO.HIGH)
        else:
            self.__led_light(GPIO.LOW, GPIO.LOW, GPIO.LOW)

    def turn_on_led(self, led):
        """打开灯

         Parameters
         ----------
         * led : int
             - LED_R  LED_G  LED_B三个选一个
         """
        print('open led')
        self.LED_FLAG[led] = True
        while self.LED_FLAG[led]:
            if led == Car.LED_R:
                GPIO.output(Car.PIN_LED_R, Car.OPEN)
            elif led == Car.LED_G:
                GPIO.output(Car.PIN_LED_G, Car.OPEN)
            else:
                GPIO.output(Car.PIN_LED_B, Car.OPEN)

    def turn_off_led(self, led):
        """关闭LED灯光

         Parameters
         ----------
         * led : int
             - LED_R  LED_G  LED_B三个选一个
         """
        self.LED_FLAG[led] = False
        if led == Car.LED_R:
            GPIO.output(Car.PIN_LED_R, Car.CLOSE)
        elif led == Car.LED_G:
            GPIO.output(Car.PIN_LED_G, Car.CLOSE)
        else:
            GPIO.output(Car.PIN_LED_B, Car.CLOSE)

    def stop_all_wheels(self, delay=0):
        """
        Stop wheel movement
        """
        time.sleep(delay)

        self.__set_motion(GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW, 0, 0)

    def stop_completely(self, delay=0):
        """
        Completely stop the Car
        """
        time.time(delay)

        self.__pwm_left_speed.stop()
        self.__pwm_right_speed.stop()
        self.__pwm_servo_ultrasonic.stop()
        GPIO.cleanup()

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
        self.__set_motion(GPIO.HIGH, GPIO.LOW, GPIO.HIGH, GPIO.LOW,
                          speed, speed, duration)

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
        self.__set_motion(GPIO.LOW, GPIO.HIGH, GPIO.LOW, GPIO.HIGH,
                          speed, speed, duration)

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
        self.__set_motion(GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.LOW,
                          0, speed, duration)

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
        self.__set_motion(GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.LOW,
                          speed, 0, duration)

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
        self.__set_motion(GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW,
                          speed, speed, duration)

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
        self.__set_motion(GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH,
                          speed, speed, duration)

    def distance_from_obstacle(self, val=0):
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
        # set HIGH at TRIG for 15us to trigger the ultrasonic ping
        print('check distance')
        # 产生一个10us的脉冲
        distance = 0
        GPIO.output(Car.PIN_TRIG, GPIO.LOW)
        time.sleep(0.02)
        GPIO.output(Car.PIN_TRIG, GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(Car.PIN_TRIG, GPIO.LOW)
        time.sleep(0.00001)

        # 等待接受
        if GPIO.input(Car.PIN_ECHO):
            distance = -2
            return distance

        time1, time2 = time.time(), time.time()

        while not GPIO.input(Car.PIN_ECHO):
            time1 = time.time()
            if time1 - time2 > 0.02:
                distance = -3
                break

        if distance == -3:
            return (distance)

        t1 = time.time()
        while GPIO.input(Car.PIN_ECHO):
            time2 = time.time()
            if time2 - t1 > 0.02:
                break

        t2 = time.time()
        distance = ((t2 - t1) * 340 / 2) * 100
        print(distance)
        return str(distance)

    def line_tracking_turn_type(self, num=4):
        """
        Indicates the type of turn required given current sensor values
        num = 4,是为了上层调用而设定

        Returns
        -------
        * str
            - one of ['sharp_left_turn', 'sharp_right_turn',
                      'regular_left_turn', 'regular_right_turn',
                      'smooth_left', 'smooth_right',
                      'straight', 'no_line']
        """
        s1_dark = GPIO.input(Car.PIN_TRACK_1) == GPIO.LOW
        s2_dark = GPIO.input(Car.PIN_TRACK_2) == GPIO.LOW
        s3_dark = GPIO.input(Car.PIN_TRACK_3) == GPIO.LOW
        s4_dark = GPIO.input(Car.PIN_TRACK_4) == GPIO.LOW

        if s1_dark and (s3_dark and s4_dark):
            #   1    2    3    4
            # Dark XXXX Dark Dark
            # Dark XXXX Dark Lite
            # Dark XXXX Lite Dark
            # Requires a sharp left turn (line bends at right or acute angle)
            turn = 'sharp_left_turn'
        elif (s1_dark or s2_dark) and s4_dark:
            #   1    2    3    4
            # Dark Dark XXXX Dark
            # Lite Dark XXXX Dark
            # Dark Lite XXXX Dark
            # Requires a sharp right turn (line bends at right or acute angle)
            turn = 'sharp_right_turn'
        elif s1_dark:
            #   1    2    3    4
            # Dark XXXX XXXX XXXX
            # Requires a regular left turn (line bends at obtuse angle)
            turn = 'regular_left_turn'
        elif s4_dark:
            #   1    2    3    4
            # XXXX XXXX XXXX Dark
            # Requires a regular right turn (line bends at obtuse angle)
            turn = 'regular_right_turn'
        elif s2_dark and not s3_dark:
            #   1    2    3    4
            # XXXX Dark Lite XXXX
            # Requires a smooth curve to the left (car veers off to the right)
            turn = 'smooth_left'
        elif not s2_dark and s3_dark:
            #   1    2    3    4
            # XXXX Lite Dark XXXX
            # Requires a smooth curve to the right (car veers off to the left)
            turn = 'smooth_right'
        elif s2_dark and s3_dark:
            #   1    2    3    4
            # XXXX Dark Dark XXXX
            # Requires going straight
            turn = 'straight'
        else:
            #   1    2    3    4
            # Lite Lite Lite Lite
            # Requires maintaining the previous movement
            turn = 'no_line'

        print('Turn type = {}'.format(turn))
        return turn

    def obstacle_status_from_infrared(self, num=0):
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
        is_left_clear = GPIO.input(Car.PIN_AVOID_LEFT_SENSOR)
        is_right_clear = GPIO.input(Car.PIN_AVOID_RIGHT_SENSOR)

        if is_left_clear and is_right_clear:
            status = 'clear'
        elif is_left_clear and not is_right_clear:
            status = 'only_right_blocked'
        elif not is_left_clear and is_right_clear:
            status = 'only_left_blocked'
        else:
            status = 'blocked'
        print('Infrared status = {}'.format(status))
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
        # 0 degrees :  duty cycle =  2.5% of 20ms
        # 90 degrees:  duty cycle =  7.5% of 20ms
        # 180 degrees: duty cycle = 12.5% of 20ms
        if dir == 'center':
            degree = 90
        elif dir == 'right':
            degree = 0
        elif dir == 'left':
            degree = 180

        for i in range(10):  # do this for multiple times just to make sure
            self.__pwm_front_servo_pos.ChangeDutyCycle(2.5 + 10 * degree / 180)
        self.__pwm_front_servo_pos.ChangeDutyCycle(0)
        time.sleep(0.02)  # give enough time to settle

    def obstacle_status_from_ultrasound(self, dir='center'):
        """
        Return obstacle status obtained by ultrasonic sensor that is
        situated in the front of the Car. The ultrasonic sensor is
        located in the upper deck so it has a higher view than the
        infrared sensors.

        Parameters
        ----------
        * dir : str
            - set the ultrasonic sensor to face a direction,
            one of ['center', 'left', 'right']. Default is 'center'

        Returns
        -------
        * str
            - 'blocked' if distance <= 20cm
            - 'approaching_obstacle' if distance is (20, 50]
            - 'clear' if distance > 50cm
        """

        self.turn_servo_ultrasonic(dir)
        distance = self.distance_from_obstacle()
        if distance <= 20:
            status = 'blocked'
        elif distance <= 50:
            status = 'approaching_obstacle'
        else:
            status = 'clear'
        print('Ultrasound status = {}'.format(status))
        return status

    def check_left_obstacle_with_sensor(self, delay=0):
        """
        利用小车左侧的红外对管传感器检测物体是否存在

        Parameters
        ----------
        * delay ：int
            - 读取稳定时间

        Returns
        -------
        * bool
            - High : 有障碍
            -Low   : 无障碍
        """
        have_obstacle = GPIO.input(Car.PIN_AVOID_LEFT_SENSOR)
        time.sleep(delay)
        if have_obstacle:
            return str(Car.NO_OBSTACLE)
        else:
            return str(Car.HAVE_OBSTACLE)

    def check_right_obstacle_with_sensor(self, delay=0):
        """
        利用小车右侧的红外对管传感器检测物体是否存在

        Parameters
        ----------
        * delay ：int
            - 读取稳定时间
        -----------
        Returns
        -------
        * bool
            - High : 有障碍
            -Low   : 无障碍
        """
        have_obstacle = GPIO.input(Car.PIN_AVOID_RIGHT_SENSOR)
        time.sleep(delay)

        if have_obstacle:
            return str(Car.NO_OBSTACLE)
        else:
            return str(Car.HAVE_OBSTACLE)

    def servo_front_rotate(self, pos):
        """控制超声波的舵机进行旋转
        舵机：SG90 脉冲周期为20ms,脉宽0.5ms-2.5ms对应的角度-90到+90，对应的占空比为2.5%-12.5%
        Parameters
        * pos: int
            - 舵机旋转的角度：0-180 度
        ----------
        * none
        Returns
        -------
        None
        """
        for i in range(Car.SERVO_TOTAL_STEP):
            self.__pwm_front_servo_pos.ChangeDutyCycle(2.5 + 10 * pos / 180)
            time.sleep(0.02)

        self.__pwm_front_servo_pos.ChangeDutyCycle(0)
        time.sleep(0.02)

    def servo_camera_rotate(self, degree):
        """调整控制相机的舵机进行旋转
        原理：舵机：SG90 脉冲周期为20ms,脉宽0.5ms-2.5ms对应的角度-90到+90，对应的占空比为2.5%-12.5%

        Parameters
        -------------
        * degree
            - 舵机旋转的角度：0 到 180 度
        ----------
        Returns
        -------
        * None
        """
        for i in range(Car.SERVO_TOTAL_STEP):
            self.__pwm_left_right_servo_pos.ChangeDutyCycle(2.5 + 10 * degree / 180)
            time.sleep(0.02)

        self.__pwm_left_right_servo_pos.ChangeDutyCycle(0)
        time.sleep(0.02)

    def servo_camera_rise_fall(self, pos):
        """舵机让相机上升和下降
        舵机：SG90 脉冲周期为20ms,脉宽0.5ms-2.5ms对应的角度-90到+90，对应的占空比为2.5%-12.5%

        Parameters
        -------------
        * pos
            - 舵机旋转的角度：0 到 180 度
        ----------
        Returns
        -------
        * None
        """
        for i in range(Car.SERVO_TOTAL_STEP):
            self.__pwm_up_down_servo_pos.ChangeDutyCycle(2.5 + 10 * pos / 180)
            time.sleep(0.02)

        self.__pwm_up_down_servo_pos.ChangeDutyCycle(0)
        time.sleep(0.02)

    @staticmethod  # 自动巡游功能
    def demo_cruising():
        """
        Demonstrates a cruising car that avoids obstacles in a room

        * Use infrared sensors and ultrasonic sensor to gauge obstacles
        * Use LED lights to indicate running/turning decisions
        """
        car = Car()
        try:
            while True:
                obstacle_status_from_infrared = car.obstacle_status_from_infrared()
                should_turn = True
                if obstacle_status_from_infrared == 'clear':
                    should_turn = False
                    obstacle_status_from_ultrasound = \
                        car.obstacle_status_from_ultrasound()
                    if obstacle_status_from_ultrasound == 'clear':
                        car.led_light('green')
                        car.run_forward(speed=10)
                    elif obstacle_status_from_ultrasound == 'approaching_obstacle':
                        car.led_light('yellow')
                        car.run_forward(speed=5)
                    else:
                        should_turn = True
                if should_turn:
                    car.run_reverse(duration=0.02)
                    if obstacle_status_from_infrared == 'only_right_blocked':
                        car.led_light('purple')
                        car.spin_left(duration=random.uniform(0.25, 1.0))
                    elif obstacle_status_from_infrared == 'only_left_blocked':
                        car.led_light('cyan')
                        car.spin_right(duration=random.uniform(0.25, 1.0))
                    else:
                        car.led_light('red')
                        car.spin_right(duration=random.uniform(0.25, 1.0))
        except KeyboardInterrupt:
            car.stop_completely()

    @staticmethod  # 自动巡线功能
    def demo_line_tracking(speed=50):
        """
        Demonstrates the line tracking mode using the line tracking sensor
        """
        time.sleep(2)
        car = Car()

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

    @staticmethod  # 输出电平，控制小车的灯的颜色
    def demo_light():
        """
        控制灯
        - one of ['red', 'green', 'blue',
          'yellow', 'cyan', 'purple'
          'white', 'off']
        """
        car = Car()
        car.led_light('red')


def main():
    rpc_car_server = zerorpc.Server(Car())
    rpc_car_server.bind("tcp://0.0.0.0:12347")
    rpc_car_server.run()


if __name__ == "__main__":
    main()
