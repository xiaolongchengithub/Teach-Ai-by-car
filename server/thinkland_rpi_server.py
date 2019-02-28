"""
    rpc服务类，将小车的api注册到服务上，就可以通过socket远程调用小车api
"""

from server.thinkland_rpi_car import Car
import socket
import threading
import time

__authors__ = 'xiao long & xu lao shi'
__version__ = 'version 0.01'
__license__ = 'Copyright...'


class Server:
    """RPC服务类
    """
    ONE_PARA = 1
    TWO_PARA = 2

    DIRECT_CALL = 1
    THREAD_CALL = 0
    RETURN_CALL = 2

    def __init__(self):
        self.car = Car()
        self.Function_List = {}
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.function_registration()

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

    def set_server_port(self, port=12347):
        """设置服务端口
        *function:set_ip
        功能：设置Ip

        Parameters
        ------------
        * port：int
            - 服务监听端口，默认为12347
        --------------
        Returns
        * None
        """

        self.socket = (self.get_ip(), 12347)
        print(self.socket)

    def function_registration(self):
        """将小车的api注册为rpc
        Parameters
        * None
        Returns
        -------
        * None
        """
        # 舵机函数注册
        self.Function_List['servo_camera_rise_fall'] = self.car.servo_camera_rise_fall
        self.Function_List['servo_camera_rotate'] = self.car.servo_camera_rotate
        self.Function_List['servo_front_rotate'] = self.car.servo_front_rotate

        # 灯的控制函数注册
        self.Function_List['turn_on_led'] = self.car.turn_on_led
        self.car.Function_List['trun_off_led'] = self.car.turn_off_led

        # 运动控制函数注册
        self.Function_List['run_forward'] = self.car.run_forward
        self.Function_List['run_reverse'] = self.car.run_reverse
        self.Function_List['turn_left'] = self.car.turn_left
        self.Function_List['turn_right'] = self.car.turn_right
        self.Function_List['spin_left'] = self.car.spin_left
        self.Function_List['spin_right'] = self.car.spin_right

        self.Function_List['demo_cruising'] = Car.demo_cruising

        # 超声波检测函数注册
        self.Function_List['distance_from_obstacle'] = self.car.distance_from_obstacle

        # 红外对管检测函数注册
        self.Function_List['check_left_obstacle_with_sensor'] = self.car.check_left_obstacle_with_sensor
        self.Function_List['check_right_obstacle_with_sensor'] = self.car.check_right_obstacle_with_sensor
        self.Function_List['obstacle_status_from_infrared'] = self.car.obstacle_status_from_infrared

        # 黑白传感器检测情况
        self.Function_List['line_tracking_turn_type'] = self.car.line_tracking_turn_type


    def star_server(self):
        """创建一个线程用于提供rpc服务
        Parameters
        * None
        ————
        Returns
        -------
        * None
        """

        server_thread = threading.Thread(None, target=self.net_call_function, args=(self.Function_List,))
        server_thread.start()

    def move_thread(self, func):
        """对运动函数的调用

        Parameters
        -----------
        * func:dict
            - 函数列表

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
        """实时网络连接

        Parameters：
        --------------
        tupple类型
        * port：网络的IP
        ————
        Returns
        -------
        * None
        """
        print("net_call_function")

        self.server.bind(self.socket)
        self.server.listen(1)
        while True:
            time.sleep(0.5)
            conn, addr = self.server.accept()
            while True:
                try:
                    data = conn.recv(1024).decode('utf-8')
                    print(data)
                    strJson = eval(data)
                    process = strJson['function']
                    mode = strJson['mode']
                    if mode == Server.THREAD_CALL:
                        move_thread = threading.Thread(None, target=self.move_thread, args=(process,))
                        move_thread.start()
                        conn.send(bytes('res ok', encoding='utf8'))

                    else:
                        if mode == Server.DIRECT_CALL:
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
                                strRe = "%s" % (re)
                                print(strRe)
                                conn.send(bytes(strRe, encoding='utf8'))
                except:
                    print('close connect')
                    conn.close()
                    break

    @staticmethod
    def demo_sever():
        """在本机上开启rpc服务
        """
        test = Server()
        test.set_server_port(12347)  # 设置Ip
        test.star_server()


def main():
    """启动服务例子
    """
    Server.demo_sever()


if __name__ == "__main__":
    main()
