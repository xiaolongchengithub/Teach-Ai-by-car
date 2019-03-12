import cv2 as cv
import numpy as np

#全局阈值

class Algrithm():
    def __init__(self):
        print("init")
        self.__DEBUG = False

    def set_debug(self):
        self.__DEBUG = True

    def switch_debug(self , status = True):
        self.__DEBUG = True

    def threshold_demo(self , image , thre = 20):
        """
        *function:threshold_demo
        功能：对图像进行二值化
        ________
        Parameters
        * image: opencv.mat类型
        * thre: 图像阀值
        ————
        Returns
        -------
        * binary 二进制图像
        """
        gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
        ret, binary = cv.threshold(gray, thre, 250, cv.THRESH_BINARY_INV)
        if self.__DEBUG:
            cv.imshow('binary',binary)
            cv.waitKey(0)
        return binary

    #局部阈值
    def local_threshold(self , image):
        """
        *function:local_threshold
        功能：对图像进行二值化 ，采用局部值域
        ________
        Parameters2
        * image: opencv.mat类型
        ————
        Returns
        -------
        * None
        """
        gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
        binary =  cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY, 25, 10)

    def line(self ,img ,thre=60, areaLimit=1000):
        """
        *function:line
        功能：从头图像中提取一条线
        ________
        Parameters
        * image: opencv.mat类型
        ————
        Returns
        -------
        * None
        """
        binary = self.threshold_demo(img,thre)
        binImg, contours, hierarchy = cv.findContours(binary, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)  # 得到轮廓信息
        contourList = []
        cx = 0.0
        cy = 0.0

        if self.__DEBUG:
            cv.drawContours(img, contours, -1, (125, 15, 125), 2)
            cv.imshow('contoure', img)
            cv.waitKey(0)

        for contour in contours:
            area = cv.contourArea(contour)
            if area > areaLimit:
                areaLimit = area
                contourList.append(contour)
                M = cv.moments(contour)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])

        print('线的中心点:(%d，%d)'%(cx,cy))

        if cx > 0:
            cv.namedWindow("camera_object", cv.WINDOW_NORMAL)
            colorImg = cv.cvtColor(binary, cv.COLOR_GRAY2RGB)
            cv.circle(colorImg,(cx,cy),20,(0,0,255),20)
            cv.imshow('camera_object', colorImg)
            cv.waitKey(1)
        return np.array([cx,cy])


"""
@@@@例子：
#测试
"""
if __name__ == "__main__":
    mat  = cv.imread('./line/line.jpg')
    ob   = Algrithm()
    ob.set_debug()
    ob.line(mat)
    # test = Figure()
    # while True:
    #     test.train() #训练