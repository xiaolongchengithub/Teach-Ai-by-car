import socket
import json
import _thread
import time
from tkinter import *
from PIL import Image, ImageTk
from PIL import ImageTk

import tkinter
import tkinter.messagebox

import socket
import cv2
import threading
import struct
import numpy
import cv2 as cv
import numpy as np

global g_camera
global g_control


#########################################################################################################
global e_user
global g_str
global g_up
global g_circle

g_str = '000'
g_up  = 45
g_circle = 90


def getUltrasonic():
    global e_user
    global g_str
    print('Ultrasonic')
    global g_control
    dis = g_control.GetDistance()
    e_user.delete(0,g_str)
    str = '%d'%dis
    g_str = str
    e_user.insert(0,str)
    print(dis)

def upCamera():
    global  g_up
    global g_control
    g_up = g_up + 10
    if g_up > 180:
        g_up = 180
    g_control.controlCameraAngle(g_up, 90,0)
    print('up')

def downCamera():
    print('down')
    global  g_up
    global g_control
    g_up = g_up - 10
    if g_up < 20:
        g_up = 20
    g_control.controlCameraAngle(g_up, 90,0)
    print('up')


def circleUpCamera():
    global  g_circle
    global g_control
    g_circle = g_circle + 10
    if g_circle > 180:
        g_circle = 180
    g_control.controlCameraAngle(45,g_circle,0)
    print('up')

def circleDownCamera():
    print('circle down')
    global  g_circle
    global g_control
    g_circle = g_circle - 10
    if g_circle < 20:
        g_circle = 20
    g_control.controlCameraAngle(45,g_circle,0)
    print('up')

class handDlg:
    def __init__(self):
        global e_user
        self.myWindow   = Tk()
        # 设置标题
        self.myWindow.title('Hand Control')
        # 设置窗口大小640
        self.width     = 250
        self.height    = 480

        # 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
        self.screenwidth  = self.myWindow.winfo_screenwidth()
        self.screenheight = self.myWindow.winfo_screenheight()
        self.gx = ('%dx%d+%d+%d'%(self.width, self.height, 640+250, 0))
        self.myWindow.geometry(self.gx)
        # 设置窗口是否可变长、宽，True：可变，False：不可变
        self.myWindow.resizable(width=False, height=True)

        self.frame_root = Frame(self.myWindow)
        # self.left       = Frame(self.frame_root)
        # self.mid        = Frame(self.frame_root)
        # self.right      = Frame(self.frame_root)

        l_user = Label(self.frame_root, text='超声波测试：')
        l_user.grid(row=0, sticky=W)

        e_user = Entry(self.frame_root,width = 12)
        e_user.grid(row=0, column=1, sticky=E)

        b_login = Button(self.frame_root, text='获取', command=getUltrasonic)
        b_login.grid(row=0, column=20, sticky=E)

        ultr = Label(self.frame_root, text='摄像头抬起：')
        ultr.grid(row=1, sticky=W)

        upbutton = Button(self.frame_root, text='up', command=upCamera,width = 6)
        upbutton.grid(row=1, column=1, sticky=E)

        downbutton = Button(self.frame_root, text='down', command=downCamera,width = 6)
        downbutton.grid(row=1, column=2, sticky=E)

        ultr1 = Label(self.frame_root, text='摄像头旋转：')
        ultr1.grid(row=2, sticky=W)

        upbutton1 = Button(self.frame_root, text='right', command=circleUpCamera,width = 6)
        upbutton1.grid(row=2, column=1, sticky=E)

        downbutton = Button(self.frame_root, text='left', command=circleDownCamera,width = 6)
        downbutton.grid(row=2, column=2, sticky=E)

        # self.speed_text = Entry(self.left, width=40)  # 30的意思是30个平均字符的宽度，height设置为两行
        # # self.speed_text.pack(padx = 0.0,pady = 40)
        # self.speed_text.grid(row=0, column=1, sticky=E)
        #
        # self.ultrasonicButton = tkinter.Button(self.mid, text="Ultrasonic", command=getUltrasonic, width=10, height=2)
        # self.speed_text['show'] = '000'
        # self.ultrasonicButton.pack(side='right',padx =10)


        #
        # self.left.pack(side='left')
        # self.mid.pack(side='left')
        # self.right.pack(side='right')
        self.frame_root.pack()



###############################################################################################################
###############################################################################################################

def linePatrol():
    global g_control
    g_control.linePatrol(10)
    print('back')

def setCtrol(val):
    global g_control
    g_control = val

def back():
    global g_control
    g_control.speedBack(5)
    print('back')

def up():
    global g_control
    g_control.speedRun(5)
    print('up')

def left():
    global g_control
    g_control.speedLeft(5)
    print('left')

def right():
    global g_control
    g_control.speedRight(5)
    print('right')

def brake():
    global g_control
    g_control.brake(0)
    print('brake')

def autoRun():
    global g_control
    g_control.autoRun(5)
    print('autoRun')

def Test():
    hand = handDlg()
    # global g_control
    # print('findObject')
    # global g_camera
    # names = g_camera.find()
    # speaker = win32com.client.Dispatch("SAPI.SpVoice")
    # if len(names) > 0:
    #     speaker.Speak("in the picture,i find a")
    # for name in names:
    #     speaker.Speak(str(name))

def SaveImage():
    global g_camera
    g_camera.saveImage('test.jpg')

def getSpeed():
    global speed_text
    data=speed_text.get() #获取文本框内容
    global s
    print('up')
    jsonText['speed']=int(data)
    mystr = str(jsonText)
        # 待发送的信息
    s.send(bytes(mystr, encoding='utf-8'))
    print('等待对方回复:')
    # 接收信息并显示
    recv_data = s.recv(1024)
    print('你有新的消息:', str(recv_data, encoding='utf-8'))
    print(data)

####################################################################################################
####################################################################################################
class dialog:
    def __init__(self):
        self.myWindow = Tk()
        # 设置标题
        self.myWindow.title('Car Control')
        # 设置窗口大小
        self.width  = 890
        self.height = 480

        # 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
        self.screenwidth  = self.myWindow.winfo_screenwidth()
        self.screenheight = self.myWindow.winfo_screenheight()
        self.gx = ('%dx%d+%d+%d'%(self.width, self.height,0, 0))
        self.myWindow.geometry(self.gx)
        # 设置窗口是否可变长、宽，True：可变，False：不可变
        self.myWindow.resizable(width=False, height=True)


        self.src = cv.imread('car.jpg')
        self.sizsrc = cv.resize(self.src, (640, 480), interpolation=cv.INTER_CUBIC)
        # 创建一个名字加 “ input image ” 的窗口，
        # 窗口可以根据图片大小自动调整
        self.img = Image.fromarray(cv.cvtColor(self.sizsrc, cv.COLOR_BGR2RGB))
        self.tkImage = ImageTk.PhotoImage(image=self.img)

        self.frame_root = Frame(self.myWindow)
        self.Frame_Img = Frame(self.frame_root, width='640', height='480')
        self.Frame_Motor = Frame(self.frame_root)

        # self.Frame_Motor['background'] = 'white'

        self.frame_speed = Frame(self.Frame_Motor, width='25', height='2')
        self.frame_1 = Frame(self.Frame_Motor)
        self.frame_2 = Frame(self.Frame_Motor)
        self.frame_3 = Frame(self.Frame_Motor)
        self.Frame_Control = Frame(self.Frame_Motor)

        self.speed_label = Label(self.frame_speed, text='speed:')
        self.speed_label.pack(side='left', padx=5)

        self.speed_text = Entry(self.frame_speed, width=10)  # 30的意思是30个平均字符的宽度，height设置为两行
        self.speed_text.pack(side='left')

        self.button_speed = tkinter.Button(self.frame_speed, text="Set", command=getSpeed, width=6, height=2)
        self.button_speed.pack(side='right', padx=20)

        self.button_control = tkinter.Button(self.Frame_Control, text="auto", command=autoRun, width=6, height=2)
        self.button_control.pack(side='top',pady = 20)

        self.button_linePatrol = tkinter.Button(self.Frame_Control, text="line", command=linePatrol, width=6, height=2)
        self.button_linePatrol.pack(side='top',pady = 0)

        self.button_control = tkinter.Button(self.Frame_Control, text="config", command=Test, width=6, height=2)
        self.button_control.pack(side='left',pady = 20)

        self.button_saveImg = tkinter.Button(self.Frame_Control, text="save", command=SaveImage, width=6, height=2)
        self.button_saveImg.pack(side='right',padx = 20)

        self.button_up = tkinter.Button(self.frame_1, text="up", command=up, width=6, height=2)
        self.button_up.pack(side='top')

        self.button_left = tkinter.Button(self.frame_2, text="left", command=left, width=6, height=2)
        self.button_left.pack(side='left')

        self.button_Null = tkinter.Button(self.frame_2, text="brake", command=brake, width=6, height=2)
        self.button_Null.pack(side='left')

        self.button_right = tkinter.Button(self.frame_2, text="right", command=right, width=6, height=2)
        self.button_right.pack(side='right')

        self.button_back = tkinter.Button(self.frame_3, text="back", command=back, width=6, height=2)
        self.button_back.pack(side='top')

        self.frame_speed.pack()
        self.frame_1.pack()
        self.frame_2.pack()
        self.frame_3.pack()
        self.Frame_Control.pack()

        self.Frame_Img.pack(side='left')
        self.Frame_Motor.pack(side='right')


        self.label = tkinter.Label(self.Frame_Img, anchor=NW,image=self.tkImage)
        self.label.pack(expand=YES, fill=BOTH)
        self.frame_root.pack()

    def setImgInput(self,input):
        testImg = Image.fromarray(input)
        testImg = ImageTk.PhotoImage(testImg)
        # self.label.imgtk = self.tkImage
        self.label.config(image=testImg)
        self.label.image = testImg

    def doModel(self):
        self.myWindow.mainloop()

    def cameraSet(self,camera):
        global g_camera
        g_camera = camera


