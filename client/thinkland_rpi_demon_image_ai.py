import carLib.thinkland_rpi_get_image as carmera
import carLib.thinkland_rpi_ai_yolov3 as yolo
import time



if __name__ == "__main__":
    ai = yolo.AiYolo()

    receiveImg = carmera.Camera()
    #连接远程网络
    receiveImg.connect_http("172.16.10.227")
    #开启数据接受
    receiveImg.start_receive_image_server()

    while True:
        #获取数据
        img = receiveImg.take_picture()
        #寻找物体
        img,id,rec = ai.find_object(img)
        #图像显示
        receiveImg.show_image(img)


