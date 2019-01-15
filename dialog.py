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

global g_control


def setCtrol(val):
    g_control = val

def back():
    print('back')


def up():
    print('up')

def left():
    print('left')

def right():
    print('right')

def brake():
    print('brake')

def autoRun():
    print('autoRun')

def FindObject():
    print('findObject')


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
        self.gx = ('%dx%d+%d+%d'%(self.width, self.height, (self.screenwidth - self.width) / 2, (self.screenheight - self.height) / 2))
        self.myWindow.geometry(self.gx)
        # 设置窗口是否可变长、宽，True：可变，False：不可变
        self.myWindow.resizable(width=False, height=True)

        self.frame_root = Frame(self.myWindow)
        self.Frame_Img = Frame(self.frame_root, width='640', height='480')
        self.Frame_Motor = Frame(self.frame_root)

        self.frame_speed = Frame(self.Frame_Motor, width='25', height='2')
        self.frame_1 = Frame(self.Frame_Motor)
        self.frame_2 = Frame(self.Frame_Motor)
        self.frame_3 = Frame(self.Frame_Motor)
        self.Frame_Control = Frame(self.Frame_Motor)

        self.speed_label = Label(self.frame_speed, text='speed:')
        self.speed_label.pack(side='left', padx=5)

        self.speed_text = Entry(self.frame_speed, width=10)  # 30的意思是30个平均字符的宽度，height设置为两行
        self.speed_text.pack(side='left')

        self.button_speed = tkinter.Button(self.frame_speed, text="Set", command=getSpeed, width=6, height=1)
        self.button_speed.pack(side='right', padx=20)

        self.button_control = tkinter.Button(self.Frame_Control, text="AutoRun", command=autoRun, width=10, height=4)
        self.button_control.pack(side='top')

        self.button_control = tkinter.Button(self.Frame_Control, text="FindObject", command=FindObject, width=10, height=4)
        self.button_control.pack(side='bottom')

        self.button_up = tkinter.Button(self.frame_1, text="up", command=up, width=10, height=4)
        self.button_up.pack(side='top')

        self.button_left = tkinter.Button(self.frame_2, text="left", command=left, width=10, height=4)
        self.button_left.pack(side='left')

        self.button_Null = tkinter.Button(self.frame_2, text="brake", command=brake, width=10, height=4)
        self.button_Null.pack(side='left')

        self.button_right = tkinter.Button(self.frame_2, text="right", command=right, width=10, height=4)
        self.button_right.pack(side='right')

        self.button_back = tkinter.Button(self.frame_3, text="back", command=back, width=10, height=4)
        self.button_back.pack(side='top')

        self.frame_speed.pack()
        self.frame_1.pack()
        self.frame_2.pack()
        self.frame_3.pack()
        self.Frame_Control.pack()

        self.Frame_Img.pack(side='left')
        self.Frame_Motor.pack(side='right')

        self.src = cv.imread('tt.jpg')
        self.sizsrc = cv.resize(self.src, (640, 480), interpolation=cv.INTER_CUBIC)
        # 创建一个名字加 “ input image ” 的窗口，
        # 窗口可以根据图片大小自动调整
        self.img = Image.fromarray(cv.cvtColor(self.sizsrc, cv.COLOR_BGR2RGB))
        self.tkImage = ImageTk.PhotoImage(image=self.img)
        self.label = tkinter.Label(self.Frame_Img, anchor=NW,image=self.tkImage)
        self.label.pack(expand=YES, fill=BOTH)
        self.frame_root.pack()


    def SetImgInput(self,input):
        testImg = Image.fromarray(input)
        testImg = ImageTk.PhotoImage(testImg)
        # self.label.imgtk = self.tkImage
        self.label.config(image=testImg)
        self.label.image = testImg





    def doModel(self):
        self.myWindow.mainloop()

