import dialog as dial
import ImgClient  as img
import carControl as car
import threading
import time

g_point = []

def UiShow():
    print('test')
    global dlg
    global img
    global control
    dlg = dial.dialog()
    dlg.doModel()




if __name__ == '__main__':

    global dlg
    global img
    global control

    dataThread = threading.Thread(target=UiShow)

    dataThread.start()

    control = car.carControl()

    control.connect()
    control.controlCameraAngle(20, 90)
    time.sleep(1)
    # control.run(8,2)
    img.setInput(dlg)
    img.connectSever()
    time.sleep(2)
    # ret = img.imgTest('cup')


    control.controlCameraAngle(45, 90)
    for num in range(10, 26):  # 迭代 10 到 20 之间的数字
        ret = img.imgTest('cup')
        if ret:
            control.run(10, 1)
            break
        else:
            control.spinLeft(10, 0.25)
        time.sleep(2)
##################################################################################run and look for
    FindObject = False
    while FindObject == False:

        control.controlCameraAngle(20, 90)
        ret = img.imgTest('cup')
        if ret == True:
            break

        control.controlCameraAngle(20, 60)
        ret = img.imgTest('cup')

        if ret == True:
            control.spinRight(10,0.5)
            control.controlCameraAngle(20, 90)
            break

        control.controlCameraAngle(20, 120)
        ret = img.imgTest('cup')
        if ret == True:
            control.spinLeft(10,0.5)
            control.controlCameraAngle(20, 90)
            break


        control.controlCameraAngle(45, 45)
        ret = img.imgTest('cup')
        if ret == True:
            control.spinRight(10, 0.5)


        control.controlCameraAngle(45, 135)
        ret = img.imgTest('cup')
        if ret == True:
            control.spinLeft(10, 0.5)

        control.controlCameraAngle(45, 90)
        ret = img.imgTest('cup')
        if ret == True:
            control.run(10, 0.5)

        control.run(10,1.5)
    while True:
        time.sleep(0.5)








