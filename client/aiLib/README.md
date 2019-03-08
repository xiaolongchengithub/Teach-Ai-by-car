# 图像分类和图像识别的区别
+ 图像分类：其基于图像的内容对图像进行标记，通常会有一组固定的标签，而你的模型必须预测出最适合图像的标签。如果给定的图像没有在标签范围内，
模型的输出结果任然是标签中最相近的一个。
+ 图像识别: 是人工智能的一个重要领域。它是指对图像进行对象识别，以识别各种不同模式的目标和对像的技术。
如果给定一张图就会从一张图片找到目标。

+ 在我们项目中，去要准确定位物体的位置，根据其位置做出相应的动作。因此我们项目需要的是物体识别。

![avatar](https://image.baidu.com/search/detail?ct=503316480&z=0&ipn=d&word=darknet%20yolov3&step_word=&hs=0&pn=8&spn=0&di=88954560652&pi=0&rn=1&tn=baiduimagedetail&is=0%2C0&istype=0&ie=utf-8&oe=utf-8&in=&cl=2&lm=-1&st=undefined&cs=1213239453%2C3585451730&os=375565468%2C3783221408&simid=0%2C0&adpicid=0&lpn=0&ln=1688&fr=&fmq=1551931520743_R&fm=&ic=undefined&s=undefined&hd=undefined&latest=undefined&copyright=undefined&se=&sme=&tab=0&width=undefined&height=undefined&face=undefined&ist=&jit=&cg=&bdtype=15&oriquery=&objurl=http%3A%2F%2Fmmbiz.qpic.cn%2Fmmbiz_jpg%2FqnVfWPYmfAgy2rELLZwRDBEne0NVe8hlD0RaZjOicFwpPBKm1uq6UFMmoiaxqt4RFDvWSjnxvzfPgz9GqwpVqQ7A%2F640%3Fwx_fmt%3Djpeg&fromurl=ippr_z2C%24qAzdH3FAzdH3F4r_z%26e3Bojtxtg_z%26e3Bqq_z%26e3Bv54AzdH3Ff%3F__ktz%3DMzUnODUyODhxNQ%3D%3D%264t1%3Dda8bamdmadacla8mcm%26t1x%3D8%26fg%3Dkbwmkckbvalvu1daakbwwvmj0kcbblaj&gsm=0&rpstart=0&rpnum=0&islist=&querylist=&force=undefined)

# 框架选择
+ 现在主流深度学习框架有Tensorflow、PyTorch, Caffe,其中Tensorflow有成熟的object detection api针对物体识别。由于我们面向的是树莓派，其速度慢，同时
面对的对象是中小学生，必须把过程简单化，因此采用了一种简单的调用方法，利用一个小型并且代码开源的c++深度学习框架Darknet,利用它进行训练，训练好模型后，通过
Opencv的DNN模块进行调用。

-  框架：Darknet Opencv


# 模型选择
+ R-CNN：，它可以说是是第一个成功将深度学习应用到目标检测上的算法。R-CNN循传统目标检测的思路，同样采用提取框，对每个框提取特征、图像分类、 非极大值抑制四个步骤进行。 一般可以在图片上使用穷举法选出所所有物体可能出现的区域框，对这些区域框提取特征并使用图像识别方法分类， 得到所有分类成功的区域后,通过非极大值抑制(Non-maximumsuppression)输出结果。
+ Fast R-CNN：对 R-CNN 的一个主要改进在于首先对整个图像进行特征抽取，然后再选取提议区域，从而减少重复计算。
+ Faster R-CNN： 对 Fast R-CNN 做了进一步改进，它将 Fast R-CNN 中的选择性搜索替换成区域提议网络（region proposal network，简称 RPN）
+ SSD：SSD的骨干网络是基于传统的图像分类网络，例如 VGG，ResNet 等。经过10个卷积层(con. layer) 和 3个池化层(max pooling) 的处理，我们可以得到一个尺寸为 38×38×512 的特征图 (feature map)。然后在这个特征图上进行回归，得到物体的位置和类别。
+ Yolov:在yolov和yolov2的基础上有yolov3，其速度更快，准确度都得到了极大的提高

* 总结：现在主流分为三种：R-CNN、SSD、Yolov及其他们的改良版，基于我们系统特点，配置一般但又需要高速，对识别率要求不是很高。我们选择了Yolvov3模型。

# 模型调用
+ https://pjreddie.com/darknet/yolo/
  的作者已经利用coco的数据集，对80种物体进行了训练，并得到yolov3.weight模型，我们在用的时候，只需利用
  Opencv的DNN模块加载模型就行。简单易用，具体的操作见thinkland_rpi_ai模块。对于没有训练的物体，则需要自己去训练。
  
# 模型训练
+ **图像采集**：这一环节在是图像训练的关键的一环，其关系到后面的模型的准确度，在采集的时候，各种光照，各种侧面，各种旋转角度
  等都考虑到。数据的来源可以利用网络资源获取，也可以利用相机实时获取。如果图片不够可以利用图像知识改变其亮度、旋转角度、增加噪音的方式，自己造一部分图片
  ；但不宜多。
  
+ **图像标注**：请查看documents文档中的“利用Darknet进行训练”

# Darknet环境搭建
##### **windows环境搭建**：VS2013、CUDA9.0 
+ 安装CUDA9.0,从https://developer.nvidia.com/cuda-toolkit-archive
  中下载。解压7.5.0cuDNN模块，从https://developer.nvidia.com/rdp/cudnn-download
  下载。
  安装CUDA，然后把cuDNN中的bin、lib、include复制到CUDA的安装目录下NVIDIA GPU Computing Toolkit\CUDA\v9.0。
  
+ 安装Vs2013

+ 下载Darknet模型 https://github.com/AlexeyAB/darknet

+ 修改darknet.sh的文件把15替换为12

+ 修改darknet.vcxproj文件，把15替换为12，把CUDA修改为CUDA9.0
 





	