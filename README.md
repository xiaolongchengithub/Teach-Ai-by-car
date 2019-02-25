# car
none
Server文件夹中：（树莓派中执行）
        thinkland_rpi_car 主要小车的基本控制函数，可以在树莓派上直接运行。可以按照  Car.demo_cruising()的例子对代码进行书写
		thinkland_rpi_sever 启动网络服务，提供远程对小车进行控制

client文件夹中：

       carLib文件夹中：
              thinkland_rpi_get_image从树莓派中获取图像,例如Camera.demo_collect_picture_windowsOrlinux
              thinkland_rpi_client 封装了小车控制的基本函数，例如运行Car.demo_ranging。但前提得提前启动thinkland_rpi_sever
	   aiLib文件中
              thinkland_rpi_ai 加载一张图片，并进行识别 ，例如demo_find_dog
              thinkland_rpi_algorithm 对图像进行基本处理，例如二值化，面积筛选等
              thinkland_rpi_figure 封装了数字识别功能,例如Figure.demo_test_figure
              thinkland_rpi_speaker语音朗读功能,如demo_say
			  
备注：yolov3.weights文件太大，需要网上下载https://pan.baidu.com/s/1e1knQGCw-jl9TBQ-z4-SOg
