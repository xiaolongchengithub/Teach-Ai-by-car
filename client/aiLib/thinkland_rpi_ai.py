import cv2
import numpy as np
import os


class Ai:
    """
    利用Yolo对物体进行识别和初步定位
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

        """
        print("path",os.path.dirname(__file__))
        if classes is None:
            classes = os.path.join(os.path.dirname(__file__), "coco/coco.names")
            print(classes)
        if config is None:
            config = os.path.join(os.path.dirname(__file__), "coco/yolov3.cfg")
        if weights is None:
            weights = os.path.join(os.path.dirname(__file__), "coco/yolov3.weights")
        self.confThreshold = 0.1  # Confidence threshold
        self.nmsThreshold = 0.6  # Non-maximum suppression threshold
        self.inpWidth = 188  # Width of network's input image
        self.inpHeight = 188  # Height of n

        self.classesFile = classes

        self.classes = None

        with open(self.classesFile, 'rt') as f:
            self.classes = f.read().rstrip('\n').split('\n')

        self.modelConfiguration = config
        self.modelWeights = weights

        self.net = cv2.dnn.readNetFromDarknet(self.modelConfiguration, self.modelWeights)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    def getOutputsNames(self):
        """Get the names of the output layers, i.e. the layers with unconnected outputs

        """
        self.layersNames = self.net.getLayerNames()
        # Get the names of the output layers, i.e. the layers with unconnected outputs
        return [self.layersNames[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    def drawPred(self, frame, classId, conf, left, top, right, bottom):
        """绘制框

        Parameters
        -------------
        * frame: numpy array
            - 图像矩阵数据
        * classId: str
            - 识别的物体名
        * left: float
            - 矩形框左上角x坐标
        * top: float
            - 矩形框左上角y坐标
        * right：float
            - 矩形框右下角x坐标
        * bottom: float
            - 矩形框右下角y坐标
        """
        try:
            left = int(round(left, 2))
            right = int(round(right, 2))
            top = int(round(top, 2))
            bottom = int(round(bottom, 2))
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255))

            label = '%.2f' % conf
            # Get the label for the class name and its confidence
            if self.classes:
                assert (classId < len(self.classes))
                label = '%s:%s' % (self.classes[classId], label)

            # Display the label at the top of the bounding box
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            top = max(top, labelSize[1])
            cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
        except:
            print("draw rect Eroor")

    def postprocess(self, frame):
        """搜素框

        Parameters
        -----------
        * frame: numpy array
            - 图像矩阵数据

        Return
        -----------
        * list:
            - 识别到所有物体的矩形框数据
        * list:
            - 识别到所有物体的名称
        """
        self.frameHeight = frame.shape[0]
        self.frameWidth = frame.shape[1]

        classIds = []
        confidences = []
        boxes = []
        # Scan through all the bounding boxes output from the network and keep only the
        # ones with high confidence scores. Assign the box's class label as the class with the highest score.
        for out in self.outs:
            for detection in out:
                scores = detection[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > self.confThreshold:
                    center_x = detection[0] * self.frameWidth
                    center_y = detection[1] * self.frameHeight
                    width = detection[2] * self.frameWidth
                    height = detection[3] * self.frameHeight
                    left = center_x - width / 2
                    top = center_y - height / 2
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])
        # Perform non maximum suppression to eliminate redundant overlapping boxes with
        # lower confidences.
        retbox = []
        retIds = []

        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.confThreshold, self.nmsThreshold)
        for i in indices:
            i = i[0]
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            # self.drawPred(frame, classIds[i], confidences[i], left, top, left + width, top + height)
            retbox.append([(left + width / 2), (top + height / 2)])
            retIds.append(self.classes[classIds[i]])
        return retbox, retIds

    def read_image(self, path):
        """读取一张图片

        Parameters
        -----------
        * path: string
            - 图片的路径

        Return
        -----------
        * image: Mat
            - Opencv的Mat图片结构
        """
        return (cv2.imread(path))

    def show_image(self, image, title='ai'):
        """图像显示

        Parameters
        -----------
        * image: Mat
            - 图像数据

        * title: str
            - 显示框的标题
        """
        return (cv2.imshow(title, image))

    def wait_key(self, delay=0):
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

    def find_object(self, frame):
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
        self.blob = cv2.dnn.blobFromImage(frame, 1 / 255, (self.inpWidth, self.inpHeight), [0, 0, 0], 1, crop=False)
        # Sets the input to the network
        self.net.setInput(self.blob)
        # Runs the forward pass to get output of the output layers
        self.outs = self.net.forward(self.getOutputsNames())
        # Remove the bounding boxes with low confidence
        box, names = self.postprocess(frame)
        return frame, names, box

    def get_rect(self, frame):
        """从图中获取训练的物体RECT

        Parameters
        -----------
        * frame: mat
            - 输入一张Mat类型图片

        Returns
        -------
        * retbox:
            - 返回检测物体的范围
        * retId:
            - 返回检测物体类型
        """
        self.blob = cv2.dnn.blobFromImage(frame, 1 / 255, (self.inpWidth, self.inpHeight), [0, 0, 0], 1, crop=False)
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
                    center_x = detection[0] * self.frameWidth
                    center_y = detection[1] * self.frameHeight
                    width = detection[2] * self.frameWidth
                    height = detection[3] * self.frameHeight
                    left = center_x - width / 2
                    top = center_y - height / 2
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])
        retbox = []
        retIds = []
        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.confThreshold, self.nmsThreshold)
        for i in indices:
            i = i[0]
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            retbox.append([(left + width / 2), (top + height / 2)])
            retIds.append(self.classes[classIds[i]])
        return retbox, retIds

    @staticmethod  #
    def demo_find_dog():
        """读取一张图片，并识别图片中的物体

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
