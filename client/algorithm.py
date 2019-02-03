import cv2 as cv
import numpy as np

global ImageData
#全局阈值
def threshold_demo(image):
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    ret, binary = cv.threshold(gray, 30, 90, cv.THRESH_BINARY_INV)
    print("threshold value %s"%ret)
    return binary

#局部阈值
def local_threshold(image):
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    binary =  cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY, 25, 10)

#用户自己计算阈值
def custom_threshold(image):
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)  #把输入图像灰度化
    h, w =gray.shape[:2]
    m = np.reshape(gray, [1,w*h])
    mean = m.sum()/(w*h)
    print("mean:",mean)
    ret, binary =  cv.threshold(gray, mean, 255, cv.THRESH_BINARY)

def line(img):
    binary = threshold_demo(img)
    binImg, contours, hierarchy = cv.findContours(binary, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)  # 得到轮廓信息
    contourList = []
    cx = 0.0
    cy = 0.0

    for contour in contours:
        area = cv.contourArea(contour)
        # print(area)
        if area > 1000:
            contourList.append(contour)
            M = cv.moments(contour)
            print(M)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            print('cx:%d' % cx)
            print('cy:%d' % cy)
    return [cx,cy]

########################################################test
# sourc = cv.imread('./test.jpg')
# line(sourc)

#
# import time
#
# class PID:
#     def __init__(self, P=0.2, I=0.0, D=0.0):
#         self.Kp = P
#         self.Ki = I
#         self.Kd = D
#         self.sample_time = 0.00
#         self.current_time = time.time()
#         self.last_time = self.current_time
#         self.clear()
#     def clear(self):
#         self.SetPoint = 0.0
#         self.PTerm = 0.0
#         self.ITerm = 0.0
#         self.DTerm = 0.0
#         self.last_error = 0.0
#         self.int_error = 0.0
#         self.windup_guard = 20.0
#         self.output = 0.0
#     def update(self, feedback_value):
#         error = self.SetPoint - feedback_value
#         self.current_time = time.time()
#         delta_time = self.current_time - self.last_time
#         delta_error = error - self.last_error
#         if (delta_time >= self.sample_time):
#             self.PTerm = self.Kp * error#比例
#             self.ITerm += error * delta_time#积分
#             if (self.ITerm < -self.windup_guard):
#                 self.ITerm = -self.windup_guard
#             elif (self.ITerm > self.windup_guard):
#                 self.ITerm = self.windup_guard
#             self.DTerm = 0.0
#             if delta_time > 0:
#                 self.DTerm = delta_error / delta_time
#             self.last_time = self.current_time
#             self.last_error = error
#             self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)
#     def setKp(self, proportional_gain):
#         self.Kp = proportional_gain
#     def setKi(self, integral_gain):
#         self.Ki = integral_gain
#     def setKd(self, derivative_gain):
#         self.Kd = derivative_gain
#     def setWindup(self, windup):
#         self.windup_guard = windup
#     def setSampleTime(self, sample_time):
#         self.sample_time = sample_time
#
# import PID
# import time
# import matplotlib
# matplotlib.use("TkAgg")
# import matplotlib.pyplot as plt
# import numpy as np
# from scipy.interpolate import spline
# #这个程序的实质就是在前九秒保持零输出，在后面的操作中在传递函数为某某的系统中输出1
#
# def test_pid(P = 0.2,  I = 0.0, D= 0.0, L=100):
#     """Self-test PID class
#
#     .. note::
#         ...
#         for i in range(1, END):
#             pid.update(feedback)
#             output = pid.output
#             if pid.SetPoint > 0:
#                 feedback += (output - (1/i))
#             if i>9:
#                 pid.SetPoint = 1
#             time.sleep(0.02)
#         ---
#     """
#     pid = PID.PID(P, I, D)
#
#     pid.SetPoint=0.0
#     pid.setSampleTime(0.01)
#
#     END = L
#     feedback = 0
#
#     feedback_list = []
#     time_list = []
#     setpoint_list = []
#
#     for i in range(1, END):
#         pid.update(feedback)
#         output = pid.output
#         if pid.SetPoint > 0:
#             feedback +=output# (output - (1/i))控制系统的函数
#         if i>9:
#             pid.SetPoint = 1
#         time.sleep(0.01)
#
#         feedback_list.append(feedback)
#         setpoint_list.append(pid.SetPoint)
#         time_list.append(i)
#
#     time_sm = np.array(time_list)
#     time_smooth = np.linspace(time_sm.min(), time_sm.max(), 300)
#     feedback_smooth = spline(time_list, feedback_list, time_smooth)
#     plt.figure(0)
#     plt.plot(time_smooth, feedback_smooth)
#     plt.plot(time_list, setpoint_list)
#     plt.xlim((0, L))
#     plt.ylim((min(feedback_list)-0.5, max(feedback_list)+0.5))
#     plt.xlabel('time (s)')
#     plt.ylabel('PID (PV)')
#     plt.title('TEST PID')
#
#     plt.ylim((1-0.5, 1+0.5))
#
#     plt.grid(True)
#     plt.show()
#
# if __name__ == "__main__":
#     test_pid(1.2, 1, 0.001, L=80)
# #    test_pid(0.8, L=50)
#
#
#
#
#

