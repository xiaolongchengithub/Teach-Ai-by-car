from tensorflow.examples.tutorials.mnist import input_data
import scipy.misc  # 图像转换使用
import os  # 文件操作
import time

# 读取MNIST数据集，如果不存在事先下载，mnist是测试集的对象
mnist = input_data.read_data_sets('./MNIST_data', one_hot=True)  # MNIST数据集所在路径
print(1)

# 把原始图片保存在MNIST_data/raw下，如果没有自动创建目录
save_dir = "MNIST_data/raw/"
if os.path.exists(save_dir) is False:
    os.makedirs(save_dir)
print(2)
# 保存前20张图片，也可以获取更多的图片ss

for i in range(20):
    # 注意，i代表第i张图片（从0开始）
    image_array = mnist.train.images[i, :]

    # 图片是784维度向量，置为28乘以28维度图像
    image_array = image_array.reshape(28, 28)

    # 保存文件的格式为：mnist_train_0.jpg... 。	将数组转化为图像
    filename = save_dir + "mnist_train_%d.jpg" % i

    # 先用scipy.misc.toimge转换为图像，再用save直接保存
    array_to_image = scipy.misc.toimage(image_array, cmin=0.0, cmax=1.0, )

    print(array_to_image)
    time.sleep(1)

    array_to_image.save(filename)  # 保
