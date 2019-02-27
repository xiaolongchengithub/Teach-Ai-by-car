# Raspberry Pi Car
#### Raspberry Pi Car 项目包含树莓派小车的客户端和服务器端所有api和demo
#### 常见问题详见[FAQ](baidu.com)

# 目录
- 1.RaspberryPi控制机器车轮 
  - [前进后退的项目](#前进后退)
  - 角度转弯的项目 
  - 合成的项目（好比正方形） 
- 2.RaspberryPi使用传感器 
  - 红外巡线行驶 
  - 红外检查障碍 
  - 超声波传感器转向
  - 超声波测距
  - 合成的项目 
    - 传感器巡线 
    - 无目的巡游
- 3.RaspberryPi使用摄像头 
  - 拍摄？（或许不用)
  - 转摄像头角度 
- 4.通过笔记本客户端实现以上项目 
  - 控制机器车轮 
    - 前进后退的项目
    - 角度转弯的项目 
    - 合成的项目 
  - 使用传感器 
    - 红外巡线行驶 
    - 红外测距
    - 超声波测距
    - 合成的项目 
      - 传感器巡线
      - 无目的巡游 
   - 使用摄像头 
     - 拍摄（视频流） 
     - 拍摄一张 
     - 转摄像头角度
- 5.机器学习图像物体识别AI项目 
  - 识别一张照片画框
  - 用摄像头拍一个照片并画框
  - 图像巡线
  - 识别数字标牌
  - 巡游通过图像物体识别寻找物体 
- 6.语音AI项目 
  - 读数发声 
  - 任务完成发声 

## 前进后退 
#### thinkland_rpi_car.py
   car.run_forward(5,10) #按照5的速度，走10s\n
   car.run_reverse(5,10) #按照5的速度，原路返回走10s
        
			  
备注：yolov3.weights文件太大，需要网上下载https://pan.baidu.com/s/1e1knQGCw-jl9TBQ-z4-SOg
