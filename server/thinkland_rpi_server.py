from thinkland_rpi_car import Car
import socket
import threading
import time

__authors__ = 'xiao long & xu lao shi'
__version__ = 'version 0.01'
__license__ = 'Copyright...'

class Server():
    """
    *在树莓派上搭建服务，提供远程调用树莓上的运动函数
    *get_ip 获取本地的IP
    *set_ip 设定ip
    *function_registration 注册函数，记录函数的地址
    *star_server 打开服务线程
    *move_thread 对某个调用开启线程服务
    *net_call_function 解析数据并调用服务
    *demo_sever @@例子启动服务

    """
    ##################宏定义
    ONE_PARA = 1
    TWO_PARA = 2

    DERECT_CALL = 1
    THREAD_CALL = 0
    RETURN_CALL = 2
    def __init__(self):
        self.car = Car()
        self.Function_List = {}

    def get_ip(self):
        """
        *function:get_ip
        功能：获取本地Ip
        """

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('www.baidu.com', 0))
            ip = s.getsockname()[0]
        except:
            ip = "x.x.x.x"
        finally:
            s.close()
        return ip

    def set_ip(self,ip):
        """
        *function:set_ip
        功能：设置Ip
        —————
        Parameters
        * ip：string
        —————
        Returns
        * None
        """
        port = "%s"%ip
        self.Ip_Port = (port,12347)
        print(self.Ip_Port)


    def function_registration(self):
        """
        *function:function_registration
        功能：用于对函数列表的注册，把函数名作为字段，映射到函数
        Parameters
        * None
        Returns
        -------
        * None
        """
        #舵机函数注册
        self.Function_List['turn_servo_camera_vertical'] = self.car.turn_servo_camera_vertical
        self.Function_List['turn_servo_camera_horizental']    = self.car.turn_servo_camera_horizental
        self.Function_List['servo_front_rotate']     = self.car.servo_front_rotate

        #灯的控制函数注册
        self.Function_List['turn_on_led'] = self.car.turn_on_led
        self.Function_List['turn_off_led'] = self.car.turn_off_led

        #运动控制函数注册
        self.Function_List['run_forward'] = self.car.run_forward
        self.Function_List['run_reverse'] = self.car.run_reverse
        self.Function_List['turn_left']   = self.car.turn_left
        self.Function_List['turn_right']  = self.car.turn_right
        self.Function_List['spin_left']   = self.car.spin_left
        self.Function_List['spin_right']  = self.car.spin_right

        self.Function_List['demo_cruising']= Car.demo_cruising

        #超声波检测函数注册
        self.Function_List['distance_from_obstacle']  = self.car.distance_from_obstacle

        #红外对管检测函数注册
        self.Function_List['check_left_obstacle_with_sensor']  = self.car.check_left_obstacle_with_sensor
        self.Function_List['check_right_obstacle_with_sensor']  = self.car.check_right_obstacle_with_sensor
        self.Function_List['obstacle_status_from_infrared'] = self.car.obstacle_status_from_infrared

        #黑白传感器检测情况
        self.Function_List['line_tracking_turn_type'] = self.car.line_tracking_turn_type


    def star_server(self):
        """
        *function:star_server
        功能：开辟一个线程用于网络服务
        Parameters
        * None
        ————
        Returns
        -------
        * None
        """
        self.function_registration()

        self.serverThread = threading.Thread(None, target=self.net_call_function, args=(self.Function_List,))
        # tart the thread
        self.serverThread.start()

    def move_thread(self, func):
        """
        *function:move_thread
        功能：对运动函数的调用
        Parameters
        * func:dict
        函数列表
        ————
        Returns
        -------
        * None
        """
        print("move_thread:")

        for key in func:
            para = func[key]
            num = len(para)

            if num == Server.ONE_PARA:
                self.Function_List[key](para[0])
            if num == Server.TWO_PARA:
                self.Function_List[key](para[0], para[1])

    def net_call_function(self, Function_List):
        """
        *function:net_call_function
        功能：时时网络连接
        Parameters：tupple类型
        * port：网络的IP
        ————
        Returns
        -------
        * None
        """
        print("net_call_function")

        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.server.bind(self.Ip_Port)
        self.server.listen(1)

        while True:
            time.sleep(0.5)
            conn,addr = self.server.accept()
            while True:
                try:
                    data     =  conn.recv(1024).decode('utf-8')
                    print((data))
                    strJson = eval(data)

                    process = strJson['function']
                    mode    = strJson['mode']

                    if mode == Server.THREAD_CALL:
                        moveThread = threading.Thread(None, target=self.move_thread, args=(process,))
                        moveThread.start()
                        conn.send(bytes('res ok', encoding='utf8'))

                    else:
                        if mode == Server.DERECT_CALL:
                            for key in process:
                                para = process[key]
                                num = len(para)

                                if num == Server.ONE_PARA:
                                    self.Function_List[key](para[0])
                                if num == Server.TWO_PARA:
                                    self.Function_List[key](para[0], para[1])
                            conn.send(bytes('res ok', encoding='utf8'))
                        else:
                            if mode == Server.RETURN_CALL:
                                print('return call')
                                for key in process:
                                    para = process[key]
                                    num = len(para)

                                    if num == Server.ONE_PARA:
                                        print('call one para')
                                        re = self.Function_List[key](para[0])
                                        print(re)
                                    if num == Server.TWO_PARA:
                                        print('call two para')
                                        re = self.Function_List[key](para[0], para[1])
                                strRe = "%s"%(re)
                                print(strRe)
                                conn.send(bytes(strRe, encoding='utf8'))
                except:
                    print('close connect')
                    conn.close()
                    break

    @staticmethod #在本地启动服务
    def demo_sever():
        """
        *function:server_demo
        功能：在本机上开启服务
        """
        test = Server()
        ip   = test.get_ip() #获取Ip
        test.set_ip(ip)#设置Ip
        test.star_server()

def main():
    """
    启动服务例子
    """
    Server().demo_sever()

"""
@@@@例子：
#在树莓派上启动小车服务
"""
if __name__ == "__main__":
    main()
