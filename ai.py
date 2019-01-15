import socket
import cv2
import threading
import struct
import numpy
import cv2 as cv
import numpy as np




class ObjectClass:
    def __init__(self,classes ="coco.names",config ="yolov3.cfg",weight = "yolov3.weights"):
        self.confThreshold = 0.6  # Confidence threshold
        self.nmsThreshold = 0.6  # Non-maximum suppression threshold
        self.inpWidth = 188  # Width of network's input image
        self.inpHeight = 188  # Height of n
        self.classesFile = classes;
        self.classes = None

        with open(self.classesFile, 'rt') as f:
            self.classes = f.read().rstrip('\n').split('\n')

        self.modelConfiguration = config;
        self.modelWeights = weight;

        self.net = cv.dnn.readNetFromDarknet(self.modelConfiguration, self.modelWeights)
        self.net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

    def getOutputsNames(self):
        self.layersNames = self.net.getLayerNames()
        # Get the names of the output layers, i.e. the layers with unconnected outputs
        return [self.layersNames[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    def drawPred(self,frame,classId, conf, left, top, right, bottom):
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
        indices = cv.dnn.NMSBoxes(boxes, confidences, self.confThreshold, self.nmsThreshold)
        for i in indices:
            i = i[0]
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            self.drawPred(frame,classIds[i], confidences[i], left, top, left + width, top + height)

    def FindObject(self,frame):
        self.blob = cv.dnn.blobFromImage(frame, 1 / 255, (self.inpWidth, self.inpHeight), [0, 0, 0], 1, crop=False)
        # Sets the input to the network
        self.net.setInput(self.blob)
        # Runs the forward pass to get output of the output layers
        self.outs = self.net.forward(self.getOutputsNames())
        # Remove the bounding boxes with low confidence
        self.postprocess(frame)
        return frame

    def GetRect(self,frame):
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



