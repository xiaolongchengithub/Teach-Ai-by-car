"""
例子：展示舵机的旋转角度，分别控制相机的上升和旋转，超声波舵机的旋转。方便实时全方位进行拍照和检测。
"""
import carLib.thinkland_rpi_car_client as car


def main():
    steer = car.carControl()
    steer.connect(('172.16.10.227', 12347))

    steer.run_forward(10,5)  #安10的速度跑5s后停止
    steer.run_reverse(10,5)
    steer.turn_left(10,5)
    steer.turn_right(10,5)
    steer.spin_left(10,5)
    steer.spin_right(10,5)

    steer.

if __name__ == "__main__":
    main()