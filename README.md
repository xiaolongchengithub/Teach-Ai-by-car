# Raspberry Pi Car
#### Raspberry Pi Car 项目包含树莓派小车的客户端和服务器端所有api和demo
#### 常见问题详见[FAQ](https://thinklandai.com/faq/index.php)

# 目录
- 一、[小车系统安装](#小车系统安装指导)
- 二、[服务端环境](#服务端环境依赖)
- 三、[客户端环境](#客户端环境依赖)
- 四、[小车服务端功能](#服务端功能)
- 五、[小车客户端功能](#客户端功能)

## 小车系统安装指导
详见[系统安装文档](https://thinklandai.com/faq/index.php)

## 服务端环境依赖
python: >=3.5
zerorpc
RPI.GPIO

## 客户端环境介绍
python: >=3.5      
opencv      
numpy
zerorpc


## 服务端功能
- 1.RaspberryPi控制机器车轮 
  - [前进后退的项目](https://github.com/GavinGaogao/Teach-Ai-by-car/tree/master/server/thinkland_rpi_car.py)
  - [角度转弯的项目](https://github.com/GavinGaogao/Teach-Ai-by-car/tree/master/server/thinkland_rpi_car.py)
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
  
## 客户端功能
- 1.通过笔记本客户端实现以下项目 
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
- 2.机器学习图像物体识别AI项目 
  - 识别一张照片画框
  - 用摄像头拍一个照片并画框
  - 图像巡线
  - 识别数字标牌
  - 巡游通过图像物体识别寻找物体 
- 3.语音AI项目 
  - 读数发声 
  - 任务完成发声 

