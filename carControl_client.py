import socket
import json
import time

class carControl:
    def __init__(self):
        self.ip_port  = ('172.16.10.227', 12347)
        self.jsonData = '{"dir":1,"speed":0,"servo":0}';
        self.jsonText = json.loads(self.jsonData)
        self.s        = socket.socket()
        self.order    = {}
# 建立连接
    def connect(self):
        self.s.connect(self.ip_port)


    def sendOrder(self,ord ={"function":[{"auto_run":[8,1]},{"auto_left":[10,2]},{"auto_right":[10,2]}],"mode":1,"speed":10,"time":10}):
        strOrder = str(ord)
        self.s.send(bytes(strOrder, encoding='utf-8'))
        print('等待对方回复:')
        # 接收信息并显示
        self.recv_data = self.s.recv(1024)
        print('你有新的消息:', str(self.recv_data, encoding='utf-8'))

    def ultrasonicServo(self,angle):
        para = [angle]
        dicPara = {}
        funPara = {}
        funPara["servo_appointed_detection"] = para
        print(type(dicPara))
        dicPara["function"]= [funPara]
        self.sendOrder(dicPara)
        time.sleep(5)

    def cameraServoCircle(self,angle):
        para = [angle]
        dicPara = {}
        funPara = {}
        funPara["servo_appointed_detection_circle"] = para
        print(type(dicPara))
        dicPara["function"]= [funPara]
        self.sendOrder(dicPara)

    def speeLeft(self,speed):
        para = [speed]
        dicPara = {}
        funPara = {}
        funPara["run_left"] = para
        print(type(dicPara))
        dicPara["function"]= [funPara]
        self.sendOrder(dicPara)


    def cameraServoUp(self,angle):
        para = [angle]
        dicPara = {}
        funPara = {}
        funPara["servo_appointed_detection_up"] = para
        print(type(dicPara))
        dicPara["function"]= [funPara]
        self.sendOrder(dicPara)


    def left(self,speed,t):
        para = [speed,t]
        dicPara = {}
        funPara = {}
        funPara["auto_left"] = para
        print(type(dicPara))
        dicPara["function"]= [funPara]
        dicPara["mode"] = 1
        self.sendOrder(dicPara)
        time.sleep(t)

    def right(self,speed,t):
        para = [speed,t]
        dicPara = {}
        funPara = {}
        funPara["auto_right"] = para
        print(type(dicPara))
        dicPara["function"]= [funPara]
        dicPara["mode"] = 1
        self.sendOrder(dicPara)
        time.sleep(t)

    def run(self,speed,t):
        para = [speed,t]
        dicPara = {}
        funPara = {}
        funPara["auto_run"] = para
        print(type(dicPara))
        dicPara["function"]= [funPara]
        dicPara["mode"] = 1
        self.sendOrder(dicPara)
        time.sleep(t)

    def back(self,speed,t):
        para = [speed,t]
        dicPara = {}
        funPara = {}
        funPara["auto_back"] = para
        print(type(dicPara))
        dicPara["function"]= [funPara]
        dicPara["mode"] = 1
        self.sendOrder(dicPara)
        time.sleep(t)

    def brake(self,speed,t):
        para = [speed,t]
        dicPara = {}
        funPara = {}
        funPara["auto_rake"] = para
        print(type(dicPara))
        dicPara["function"]= [funPara]
        dicPara["mode"] = 1
        self.sendOrder(dicPara)
        time.sleep(t)

    def spinLeft(self,speed,t):
        para = [speed,t]
        dicPara = {}
        funPara = {}
        funPara["auto_spin_left"] = para
        print(type(dicPara))
        dicPara["function"]= [funPara]
        dicPara["mode"] = 1
        self.sendOrder(dicPara)
        time.sleep(t)


    def spinRight(self,speed,t):
        para = [speed,t]
        dicPara = {}
        funPara = {}
        funPara["auto_spin_right"] = para
        print(type(dicPara))
        dicPara["function"]= [funPara]
        dicPara["mode"] = 1
        self.sendOrder(dicPara)
        time.sleep(t)

    def controlCameraAngle(self,up,circle):
        self.cameraServoUp(up)
        self.cameraServoCircle(circle)
        time.sleep(2)


def hand(a):
    print(('test',a))
















