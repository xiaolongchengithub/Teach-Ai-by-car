import carLib.thinkland_rpi_get_image as carmera
import carLib.thinkland_rpi_ai_yolov3 as yolo
import time

ai = yolo.AiYolo()

receiveImg = carmera.Camera()
receiveImg.connect_http("172.16.10.227")
receiveImg.start_receive_image_server()


time.sleep(2)
while True:
    img = receiveImg.take_picture()
    img,id,rec = ai.find_object(img)
    receiveImg.show_image(img)
