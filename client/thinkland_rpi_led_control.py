"""
例子：控制Led的彩色灯，分为红、黄、绿。下命是分别打开红黄绿三种灯的例子。
在下面的实现是通过一个线程来控制，一个灯是用一个线程实时进行控制。所以灯是并发处理的
"""
import carLib.thinkland_rpi_car_client as car
import time

##########################打开红灯
def Open_Red_Led():
    led = car.carControl()
    led.connect(('172.16.10.227', 12347))
    led.close_all_led()
    led.open_led(car.LED_R)


##########################打开红灯
def Open_Green_Led():
    led = car.carControl()
    led.connect(('172.16.10.227', 12347))
    led.close_all_led()
    led.open_led(car.LED_G)

##########################打开红灯
def Open_Blue_Led():
    led = car.carControl()
    led.connect(('172.16.10.227', 12347))
    led.close_all_led()
    led.open_led(car.LED_B)

Open_Red_Led()