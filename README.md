# car
＃thinklandml201包

##关于包得说明
包分为两部分，Server需要部署到树莓派上；Client需要部署到linux或windows上。
###Server:包含thinkland_rpi_car和thinkland_rpi_sever两大模块。
###Client:包含thinkland_rpi_car_client和thinkland_rpi_camera_client,thinkland_rpi_ai,thinkland_rpi_algorithm,thinkland_rpi_figure等模块


## API文档
查找每个模块的*.html文档


##操作流程
    1、配置树莓派网络，确保树莓派和客服端在同一个网关之中；
	2、获取树莓派的Ip （ifconfig命令）；
	3、启动thinkland_rpi_sever.py(python3 thinkland_rpi_server.py)；
	4、在客服端实现各种功能；

	
##小车介绍  thinkland_rpi_car_client模块中
###操作小车上的RGB彩色灯
     Car.demo_led_switch()展示了Led的显示和关闭
	 
###控制小车 直行 转弯 等操作
     Car.demo_car_moving()
	 
###测试小车上的传感器
     Car.demo_sensor() 红外对管 黑白传感器 超声波三种测试
	 
###组合运动
     Car.demo_cruising() 利用超声波和红外对管实现超声波
	 Car.demo_line_tracking() 利用黑白传感器实现巡线功能
	 
##小车智能
###获取图像 thinkland_rpi_camera_client模块中
     Camera.demo_collect_picture_windowsOrlinux()图像显示
	 Camera.demo_only_take_picture() 图像显示，并获取图像
	 
###数字识别 thinkland_rpi_figure
     Figure.demo_test_figure()
	  
###物体识别 thinkland_rpi_ai
     Ai.demo_find_dog()

###语音朗读
     Speaker.demo_say()
	 

##给小车赋予人的智慧----智慧车
##智能相机
thinkland_rpi_ai_camera 模块

##摇头晃脑--寻找物体 
thinkland_rpi_demo_still_find_object 模块



			  
备注：yolov3.weights文件太大，需要网上下载https://pan.baidu.com/s/1e1knQGCw-jl9TBQ-z4-SOg
