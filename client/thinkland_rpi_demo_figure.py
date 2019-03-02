from carLib.thinkland_rpi_camera_client import Camera
from aiLib.thinkland_rpi_ai import  Ai
import cv2
import time
import threading
from aiLib.thinkland_rpi_speaker import Speaker
from aiLib.thinkland_rpi_figure import Figure


global figureImage
global figure
x1  = 0
y1  = 0
x2  = 0
y2  = 0


def OnMouseAction(event, x, y, flags, param):
    """
     按键响应
    """
    global figureImage
    global x1
    global y1
    global x2
    global y2
    global figure
    if event == cv2.EVENT_RBUTTONDOWN:
        print("左键点击1")
        cropImg = figureImage[y1+1:y2-1, x1+1:x2-1]
        # cv2.imshow('crop',cropImg)
        # cv2.waitKey(0)
        cv2.imwrite('./tt.jpg',cropImg)
        mat = figure.convert_mat_to_image(cropImg)
        num = figure.find_figure(mat)
        print(num)
        x1,y1,x2,y2 = 0,0,0,0
    if event == cv2.EVENT_LBUTTONDOWN:
        print("左键点击1")
        x1, y1 = x, y
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        x2 = x
        y2 = y

class cameraFigure():
    """
    现在只是针对windows llinux
    制作智能相机，识别视野中的物体
    """
    global figure
    def __init__(self ,ip = "172.16.10.227"):
        """
        初始化，区别coco.names;yolov3.cfg;yolov3.weights文件放在aiLib文件夹中;
        启动相机服务


        Parameter
        --------
             --ip string类型，default "172.16.10.227" ，
        """
        global figure
        figure = Figure()
        figure.load_model("model\model.ckpt")

        print("init camera")
        self.camera = Camera()

        self.camera = Camera()
        self.camera.connect_server(ip)
        self.camera.start_receive()

        self.ai = Ai(classes="./aiLib/coco/coco.names",config ="./aiLib/coco/yolov3.cfg",weight = "./aiLib/coco/yolov3.weights")
        self.speaker = Speaker()


    def show(self):
        """
        获取相机，实时检测，图像显示
        """
        global figureImage
        cv2.namedWindow('ai')
        cv2.setMouseCallback('ai', OnMouseAction)
        while True:
            figureImage     = self.camera.take_picture()
            blue = (255, 0, 0)  # 18
            cv2.rectangle(figureImage, (x1, y1), (x2, y2), blue, 1)  # 19
            cv2.imshow("ai",figureImage)
            cv2.waitKey(1)
            # mat = self.figure.convert_mat_to_image(figureImage)
            # num     = self.figure.find_figure(mat)
            # print(num)

    def start_thread_ai_camera(self):
        """
        启动线程
        """
        self.mainThread = threading.Thread(target=self.show)
        self.mainThread.start()


    @staticmethod
    def demo():
        """
        制作智能相机
        """
        camera = cameraFigure("172.16.10.227")
        time.sleep(1)
        camera.start_thread_ai_camera()

def main():
    """
    例子
    """
    cameraFigure.demo()

if __name__ == "__main__":
    main()


