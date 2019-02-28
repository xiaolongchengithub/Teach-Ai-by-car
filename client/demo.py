import cv2
import numpy as np

mode = 0

#创建回调函数
def OnMouseAction(event,x,y,flags,param):
    global x1, y1

    if mode == 0 and event == cv2.EVENT_LBUTTONDOWN:
        print("左键点击")
        cv2.line(img,(0,0),(x,y),(255,255,0),2)

    if mode == 1 and event == cv2.EVENT_LBUTTONDOWN:
        print("左键点击1")
        x1, y1 = x, y
    elif mode == 1 and event==cv2.EVENT_MOUSEMOVE and flags ==cv2.EVENT_FLAG_LBUTTON:
        print("左鍵拖曳1")
        cv2.rectangle(img,(x1,y1),(x,y),(0,255,0),-1)

'''
下面把回调函数与OpenCV窗口绑定在一起
'''
img = np.zeros((500,500,3),np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image',OnMouseAction)
while(1):
    cv2.imshow('image',img)
    k=cv2.waitKey(1)
    if k==ord('l'):
        mode = 0
    elif k==ord('t'):
        mode = 1
    elif k==ord('q'):
        break
cv2.destroyAllWindows()
# import cv2
# import numpy as np
#
# #创建回调函数
# def OnMouseAction(event,x,y,flags,param):
#
#     if event == cv2.EVENT_LBUTTONDOWN:
#         print("左键点击")
#     elif event==cv2.EVENT_RBUTTONDOWN :
#         print("右键点击")
#     elif flags==cv2.EVENT_FLAG_LBUTTON:
#         print("左鍵拖曳")
#     elif event==cv2.EVENT_MBUTTONDOWN :
#         print("中键点击")
#
# '''
# 创建回调函数的函数setMouseCallback()；
# 下面把回调函数与OpenCV窗口绑定在一起
# '''
# img = np.zeros((500,500,3),np.uint8)
# cv2.namedWindow('image')
# cv2.setMouseCallback('image',OnMouseAction)
# cv2.imshow('image',img)
# cv2.waitKey(30000)
# cv2.destroyAllWindows()
# # -*- coding: utf-8 -*-
#
# import cv2
# import numpy as np
#
#
# def nothing(x):
#     pass
#
#
# # 创建一副黑色图像
# img = np.zeros((300, 512, 3), np.uint8)
#
# # 设置滑动条组件
# cv2.namedWindow('image')
# cv2.createTrackbar('R', 'image', 0, 255, nothing)
# cv2.createTrackbar('G', 'image', 0, 255, nothing)
# cv2.createTrackbar('B', 'image', 0, 255, nothing)
# # 开关,控制是否启用滑动条
# switch = '0:OFF\n1:ON'
# cv2.createTrackbar(switch, 'image', 0, 1, nothing)
#
# while (1):
#     cv2.imshow('image', img)
#     k = cv2.waitKey(1) & 0xFF
#     if k == 27:
#         break
#
#     r = cv2.getTrackbarPos('R', 'image')
#     g = cv2.getTrackbarPos('G', 'image')
#     b = cv2.getTrackbarPos('B', 'image')
#     s = cv2.getTrackbarPos(switch, 'image')
#     if s == 0:
#         img[:] = 0
#     else:
#         img[:] = [b, g, r]
#
# # 销毁窗口
# cv2.destroyAllWindows()