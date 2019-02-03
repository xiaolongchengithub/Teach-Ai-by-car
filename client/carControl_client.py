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

    def GetDistance(self):
        para = [0]
        dicPara = {}
        funPara = {}
        funPara["Distance_test"] = para
        dicPara["function"]= [funPara]
        dicPara["mode"]   = 3
        dis = self.sendOrder(dicPara)
        dis = int(dis)
        return dis

    def GetIoLeft(self):
        para = [0]
        dicPara = {}
        funPara = {}
        funPara["GetIoLeft"] = para
        dicPara["function"]= [funPara]
        dicPara["mode"]   = 3
        io = self.sendOrder(dicPara)
        io = int(io)
        return io

    def GetIoRight(self):
        para = [0]
        dicPara = {}
        funPara = {}
        funPara["GetIoRight"] = para
        dicPara["function"]= [funPara]
        dicPara["mode"]   = 3
        io = self.sendOrder(dicPara)
        io = int(io)
        return io

    def connect(self,port):
        self.s.connect(port)


    def sendOrder(self,ord ={"function":[{"auto_run":[8,1]},{"auto_left":[10,2]},{"auto_right":[10,2]}],"mode":1,"speed":10,"time":10}):
        strOrder = str(ord)
        self.s.send(bytes(strOrder, encoding='utf-8'))
        # print('等待对方回复:')
        # 接收信息并显示
        self.recv_data = self.s.recv(1024)
        return self.recv_data
        print('你有新的消息:', str(self.recv_data, encoding='utf-8'))

    def ultrasonicServo(self,angle):
        para = [angle]
        dicPara = {}
        funPara = {}
        funPara["servo_appointed_detection"] = para
        print(type(dicPara))
        dicPara["function"]= [funPara]
        dicPara["mode"]   = 1
        self.sendOrder(dicPara)
        time.sleep(5)

    def cameraServoCircle(self,angle):
        para = [angle]
        dicPara = {}
        funPara = {}
        funPara["servo_appointed_detection_circle"] = para
        dicPara["function"]= [funPara]
        dicPara["mode"]   = 1
        self.sendOrder(dicPara)

    def speedLeft(self,speed):
        para = [speed]
        dicPara = {}
        funPara = {}
        funPara["left"] = para
        dicPara["function"]= [funPara]
        dicPara["mode"]   = 0
        self.sendOrder(dicPara)

    def speedRight(self,speed):
        para = [speed]
        dicPara = {}
        funPara = {}
        funPara["right"] = para
        dicPara["function"]= [funPara]
        dicPara["mode"]   = 0
        self.sendOrder(dicPara)

    def speedBack(self,speed):
        para = [speed]
        dicPara = {}
        funPara = {}
        funPara["back"] = para
        dicPara["function"]= [funPara]
        dicPara["mode"]   = 0
        self.sendOrder(dicPara)

    def speedRun(self,speed):
        para = [speed]
        dicPara = {}
        funPara = {}
        funPara["run"] = para
        dicPara["function"]= [funPara]
        dicPara["mode"]   = 0
        self.sendOrder(dicPara)

    def speedRunSpin(self,leftSpeed,rightSpeed):
        para = [leftSpeed,rightSpeed]
        dicPara = {}
        funPara = {}
        funPara["runSpin"] = para
        dicPara["function"]= [funPara]
        dicPara["mode"]    = 0
        self.sendOrder(dicPara)

    def speedSpinLeft(self,speed):
        para = [speed]
        dicPara = {}
        funPara = {}
        funPara["run"] = para
        dicPara["function"]= [funPara]
        dicPara["mode"]   = 0
        self.sendOrder(dicPara)

    def speedSpinRight(self,speed):
        para = [speed]
        dicPara = {}
        funPara = {}
        funPara["run"] = para
        dicPara["function"]= [funPara]
        dicPara["mode"]   = 0
        self.sendOrder(dicPara)

    def cameraServoUp(self,angle):
        para = [angle]
        dicPara = {}
        funPara = {}
        funPara["servo_appointed_detection_up"] = para
        dicPara["function"]= [funPara]
        dicPara["mode"]   = 1
        self.sendOrder(dicPara)


    def left(self,speed,t):
        para = [speed,t]
        dicPara = {}
        funPara = {}
        funPara["auto_left"] = para
        dicPara["function"]= [funPara]
        dicPara["mode"] = 1
        self.sendOrder(dicPara)
        time.sleep(t)

    def right(self,speed,t):
        para = [speed,t]
        dicPara = {}
        funPara = {}
        funPara["auto_right"] = para
        dicPara["function"]= [funPara]
        dicPara["mode"] = 1
        self.sendOrder(dicPara)
        time.sleep(t)

    def run(self,speed,t):
        para = [speed,t]
        dicPara = {}
        funPara = {}
        funPara["auto_run"] = para
        dicPara["function"]= [funPara]
        dicPara["mode"] = 1
        self.sendOrder(dicPara)
        time.sleep(t)

    def back(self,speed,t):
        para = [speed,t]
        dicPara = {}
        funPara = {}
        funPara["auto_back"] = para
        dicPara["function"]= [funPara]
        dicPara["mode"] = 1
        self.sendOrder(dicPara)
        time.sleep(t)

    def brake(self,speed):
        para = [speed]
        dicPara = {}
        funPara = {}
        funPara["stop"] = para
        dicPara["function"]= [funPara]
        dicPara["mode"] = 0
        self.sendOrder(dicPara)


    def spinLeft(self,speed,t):
        para = [speed,t]
        dicPara = {}
        funPara = {}
        funPara["auto_spin_left"] = para
        dicPara["function"]= [funPara]
        dicPara["mode"] = 1
        self.sendOrder(dicPara)
        time.sleep(t)

    def autoRun(self,speed):
        para = [speed]
        dicPara = {}
        funPara = {}
        funPara["AutoRun"] = para
        dicPara["function"]= [funPara]
        dicPara["mode"] = 1
        self.sendOrder(dicPara)

    def linePatrol(self,speed):
        para    = [speed]
        dicPara = {}
        funPara = {}
        funPara["linePatrol"] = para
        dicPara["function"]   = [funPara]
        dicPara["mode"]       = 1
        self.sendOrder(dicPara)


    def spinRight(self,speed,t):
        para = [speed,t]
        dicPara = {}
        funPara = {}
        funPara["auto_spin_right"] = para
        dicPara["function"]= [funPara]
        dicPara["mode"]   = 1
        self.sendOrder(dicPara)
        time.sleep(t)

    def controlCameraAngle(self,up,circle,t=2):
        self.cameraServoUp(up)
        self.cameraServoCircle(circle)
        time.sleep(t)


    def stopAutoRun(self):
        para = [False]
        dicPara                 = {}
        funPara                 = {}
        funPara["stop_autoRun"] = para
        dicPara["function"]     = [funPara]
        dicPara["mode"]         = 0
        self.sendOrder(dicPara)



def hand(a):
    print(('test',a))
















