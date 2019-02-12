import dialog as dial
import ImgClient  as camera
import carControl_client as car
import threading
import time
import serverLog as logServer
import logging
import logging.handlers

g_point = []

global dlg
global camera
global control
global bShow

rootLogger = logging.getLogger('')
rootLogger.setLevel(logging.DEBUG)

def UiShow():
    print('test')
    global dlg
    global control
    dlg = dial.dialog()
    dlg.doModel()




def init(carPort,imgPort,localIp,show = True):
    global dlg
    global camera
    global control

    logServer.startLogServer(localIp)
    if show:
        dataThread = threading.Thread(target=UiShow)
        dataThread.start()
    else:
        dlg = dial.dialog()

    control = car.carControl()
    control.connect(carPort)
    control.controlCameraAngle(20, 90)
    time.sleep(1)
    # control.run(8,2)
    camera.setInput(dlg,control,show)
    camera.connectSever(imgPort)
    dial.setCtrol(control)
    if show:
        dlg.cameraSet(camera)

    # ret = camera.imgTest('cup')









