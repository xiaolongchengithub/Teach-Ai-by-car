"""
例子：展示舵机的旋转角度，分别控制相机的上升和旋转，超声波舵机的旋转。方便实时全方位进行拍照和检测。
"""
import carLib.thinkland_rpi_car_client as car

steer = car.carControl()
steer.connect(('172.16.10.227', 12347))


steer.servo_camera_rotate(90)