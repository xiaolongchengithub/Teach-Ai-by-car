import socket
import cv2
import threading
import struct
import cv2 as cv
import numpy as np
import os

class Ai:
    """
    利用Yolo对物体进行识别和初步定位
    *__init__ 初始化*.names文件 yolov3.cfg文件  yolov3.weights文件文件进行加载和初始化
    *getOutputsNames 获取对应names
    *drawPred 对Rect进行绘制
    *read_image 读取图片
    *wait_key 等待
    """
    def __init__(self, classes=None, config=None, weights=None):
        """
        *function:__init_
        Parameters
        ----------
        classes: path to the file containing classification names.
        config: path to the file containing yolov3 configuration.
        weights: path to the file containing yolov3 model weights

        Defaults refer to coco.names, yolov3.cfg, yolov3.weights all installed in the package containing this module

        功能：初始化注意需要把coco.names,yolov3.cfg,yolov3.weights文件拷贝到当前目录.如果没有在当前目录，需要指定路径
        ________
        """
        if classes is None:
            classes = os.path.join(os.path.dirname(__file__), "./coco.names")
        if config is None:
            config  = os.path.join(os.path.dirname(__file__), "./yolov3.cfg")
        if weights is None:
            weights  = os.path.join(os.path.dirname(__file__), "./yolov3.weights")
        self.confThreshold = 0.1  # Confidence threshold
        self.nmsThreshold = 0.6  # Non-maximum suppression threshold
        self.inpWidth = 188  # Width of network's input image
        self.inpHeight = 188  # Height of n
        self.classesFile = classes;
        self.classes = None

        with open(self.classesFile, 'rt') as f:
            self.classes = f.read().rstrip('\n').split('\n')

        self.modelConfiguration = config;
        self.modelWeights = weights;

        self.net = cv.dnn.readNetFromDarknet(self.modelConfiguration, self.modelWeights)
        self.net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

    def getOutputsNames(self):
        """
        *function:getOutputsNames
        功能：Get the names of the output layers, i.e. the layers with unconnected outputs
        ________
        """
        self.layersNames = self.net.getLayerNames()
        # Get the names of the output layers, i.e. the layers with unconnected outputs
        return [self.layersNames[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    def drawPred(self,frame,classId, conf, left, top, right, bottom):
        """
        *function:drawPred
        功能：绘制框
        ________
        """
        # Draw a bounding box.
        cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255))

        label = '%.2f' % conf

        # Get the label for the class name and its confidence
        if self.classes:
            assert (classId < len(self.classes))
            label = '%s:%s' % (self.classes[classId], label)

        # Display the label at the top of the bounding box
        labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        top = max(top, labelSize[1])
        cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))

    def postprocess(self,frame):
        """
        *function:postprocess
        功能：搜素框
        ________
        """
        self.frameHeight = frame.shape[0]
        self.frameWidth = frame.shape[1]

        classIds = []
        confidences = []
        boxes = []
        # Scan through all the bounding boxes output from the network and keep only the
        # ones with high confidence scores. Assign the box's class label as the class with the highest score.
        classIds = []
        confidences = []
        boxes = []

        for out in self.outs:
            for detection in out:
                scores = detection[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence >self.confThreshold:
                    center_x = int(detection[0] * self.frameWidth)
                    center_y = int(detection[1] * self.frameHeight)
                    width = int(detection[2] * self.frameWidth)
                    height = int(detection[3] * self.frameHeight)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])
        # Perform non maximum suppression to eliminate redundant overlapping boxes with
        # lower confidences.
        retbox = []
        retIds = []
        indices = cv.dnn.NMSBoxes(boxes, confidences, self.confThreshold, self.nmsThreshold)
        for i in indices:
            i = i[0]
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            self.drawPred(frame,classIds[i], confidences[i], left, top, left + width, top + height)
            retbox.append([(left+width/2),(top+height/2)])
            retIds.append(self.classes[classIds[i]])
        return retbox,retIds

    def read_image(self , path):
        """
        *function:read_image
        功能：读取一张图片
        ________
        Parameters
        * path: string
        图片的路径
        ————
        Return
        *image:Mat
        Opencv的Mat图片结构
        """
        return (cv2.imread(path))

    def show_image(self ,image , title = 'ai'):
        """
        *function:show_image
        功能：图像显示
        ________
        Parameters
        * path: Mat
        图像数据

        *title:String
        显示框的标题
        """
        return (cv2.imshow(title,image))

    def wait_key(self , delay = 0):
        """
        *function:wait_key
        功能：图片显示等待时间
        ________
        Parameters
        * path: delay
        图片延时等待时间。如果为0，就需要
        ————
        Return
        *image:Mat
        Opencv的Mat图片结构
        """
        return (cv2.waitKey(delay))

    def find_object(self,frame):
        """
        *function:find_object
        功能：从图中获取训练的物体RECT
        ________
        Parameters
        * frame: opencv.mat类型
        输入一张Mat类型图片
        ————
        Returns
        -------
        * frame
        返回绘制了画检测物体的图片
        *names
        返回检测物体类型
        *box
        返回检测物体的RECT
        """
        self.blob = cv.dnn.blobFromImage(frame, 1 / 255, (self.inpWidth, self.inpHeight), [0, 0, 0], 1, crop=False)
        # Sets the input to the network
        self.net.setInput(self.blob)
        # Runs the forward pass to get output of the output layers
        self.outs = self.net.forward(self.getOutputsNames())
        # Remove the bounding boxes with low confidence
        box,names = self.postprocess(frame)
        return frame,names,box

    def get_rect(self,frame):
        """
        *function:get_rect
        功能：从图中获取训练的物体RECT
        ________
        Parameters
        * frame: opencv.mat类型
        输入一张Mat类型图片
        ————
        Returns
        -------
        * retbox
        返回检测物体的范围
        *retId
        返回检测物体类型
        """
        self.blob = cv.dnn.blobFromImage(frame, 1 / 255, (self.inpWidth, self.inpHeight), [0, 0, 0], 1, crop=False)
        # Sets the input to the network
        self.net.setInput(self.blob)
        # Runs the forward pass to get output of the output layers
        self.outs = self.net.forward(self.getOutputsNames())

        classIds = []
        confidences = []
        boxes = []

        self.frameHeight = frame.shape[0]
        self.frameWidth = frame.shape[1]

        for out in self.outs:

            for detection in out:
                scores = detection[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > self.confThreshold:
                    center_x = int(detection[0] * self.frameWidth)
                    center_y = int(detection[1] * self.frameHeight)
                    width = int(detection[2] * self.frameWidth)
                    height = int(detection[3] * self.frameHeight)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])
        retbox = []
        retIds = []
        indices = cv.dnn.NMSBoxes(boxes, confidences, self.confThreshold, self.nmsThreshold)
        for i in indices:
            i = i[0]
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            retbox.append([(left+width/2),(top+height/2)])
            retIds.append(self.classes[classIds[i]])
        return retbox,retIds

    @staticmethod #
    def demo_find_dog():
        """
        读取一张图片，并识别图片中的物体
        """
        test = Ai()
        # 加载图片
        img = test.read_image(".//dog.jpg")
        # 寻找物体
        ret, id, rec = test.find_object(img)
        print(id)
        # 显示
        test.show_image(ret)
        # 等待
        test.wait_key(0)
"""
@@@@例子：
#
"""
if __name__ == "__main__":
    Ai.demo_find_dog()




