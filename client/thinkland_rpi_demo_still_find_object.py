from carLib.thinkland_rpi_camera_client import Camera
from carLib.thinkland_rpi_car_client import Car
from aiLib.thinkland_rpi_ai import  Ai

from aiLib.thinkland_rpi_speaker import Speaker
import time


def main():
    str = "172.16.10.227" #= input("请输入树莓派的IP:")
    camera = Camera()
    camera.connect_http(str)
    camera.start_receive_image_server()
    camera.open_window()

    car = Car()
    car.connect(str)

    ai = Ai(classes="./aiLib/coco.names",config ="./aiLib/yolov3.cfg",weight = "./aiLib/yolov3.weights")

    speaker = Speaker()

    car.turn_servo_camera_vertical(30)

    for angle in range(20,180,20):
        car.turn_servo_camera_horizental(angle)
        time.sleep(1)
        picture = camera.take_picture()
        _,names,_ = ai.find_object(picture)
        print(names)
        for item in names:
            if item == 'cup':
                speaker.say("find a cup")
                camera.http_close()
                return
        camera.http_close()

if __name__ == "__main__":
    main()


