from PIL import Image, ImageFilter
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import cv2
import cv2 as cv
import matplotlib.pyplot as plt

"""
模块功能：识别图片数字，模型的目录为当前目录
"""
def threshold_demo(image):
    """
    *function:threshold_demo
    功能：对图像进行二值化
    ________
    Parameters
    * image: opencv.mat类型
    ————
    Returns
    -------
    * None
    """
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    ret, binary = cv.threshold(gray, 2, 250, cv.THRESH_BINARY)
    print("threshold value %s"%ret)
    return binary

class Figure():
    def __init__(self):
        print('figure init')


    def weight_variable(self,shape):
        """
        *function:weight_variable
        功能：这个函数产生正太分布，均值和标准差自己设定。这是一个截断的产生正太分布的函数，
        就是说产生正太分布的值如果与均值的差值大于两倍的标准差，那就重新生成。
        和一般的正太分布的产生随机数据比起来，这个函数产生的随机数与均值的差距不会超过两倍的标准差，
        但是一般的别的函数是可能的。

        ________
        Parameters
        * shape : 张量
        - 生成张量的维度
        ————
        Returns
        -------
        * tensor
        指定维度的正太分布的张量
        """
        initial = tf.truncated_normal(shape, stddev = 0.1)
        return tf.Variable(initial)

    def bias_variable(self, shape):
        """
        *function:bias_variable
        功能：生成一个常量
        ________
        Parameters
        * shape : 张量
        - 张量的维度
        ————
        Returns
        -------
        * tf.Value
        指定维度的正太分布的张量
        """
        initial = tf.constant(0.1,shape = shape)
        return tf.Variable(initial)

    def conv2d(self , x, W):
        """
        *function:conv2d
        功能：对图像进行卷积运算
        ________
        Parameters
        * x : Tensor
        - 一张图像数据
        *W :Tensor
        -卷积的卷积核
        ————
        Returns
        -------
        * Tensor
        特征提取后的图像数据，格式为[batch, height, width, channels]
        """
        return tf.nn.conv2d(x, W, strides = [1,1,1,1], padding = 'SAME')

    def max_pool_2x2(self , x):
        """"
        *function: max_pool_2x2
        功能：CNN当中的最大值池化操作，
        ________
        Parameters
        *x: Tensor
        - 卷积后的特征 格式为[batch, height, width, channels]

        ————
        Returns
        -------
        *Tensor
        特征提取后的图像数据，格式为[batch, height, width, channels]
        """
        return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')

    def read_image(self , path):
        """"
        *function: read_image
        功能：利用 PIL读取图片，
        ________
        Parameters
        *x: path：string
        - 图片的路径
        ————
        Returns
        -------
        *img:PIL.Image.Image
        """
        im = Image.open(path) #读取的图片
        return im

    def convert_mat_to_image(self ,mat):
        """
        *function:convert_mat_to_image
        功能：把Opencv的数据结构Mat 转换为 PIL
        _________
        Parameters
        *x: Opencv mat
        - 图片的路径
        ————
        Returns
        -------
        *img:PIL.Image.Image
        """
        image = Image.fromarray(cv2.cvtColor(mat, cv2.COLOR_BGR2RGB))
        return image

    def find_figure(self , im):
        # im = Image.open('D:./6.jpg')
        data = im.resize((28, 28), Image.ANTIALIAS)#转换为28*28像素
        plt.imshow(im)  #显示需要识别的图片
        # plt.show()
        data = data.convert('L')
        tv = list(data.getdata())
        tva = [(255-x)*1.0/255.0 for x in tv]
        result = tva
        predint = self.prediction.eval(feed_dict={self.x: [result], self.keep_prob: 1.0}, session=self.sess)
        print('识别结果:')
        print(predint)
        return predint[0]

    def load_model(self,path = "model/model.ckpt"):
        """
        *function:imageprepare
        功能:对图片进行数字识别的模型和训练文件
        ________
        Parameters
        * None
        ————
        Returns
        -------
        * None
        """
        self.x = tf.placeholder(tf.float32, [None, 784])
        self.y_ = tf.placeholder(tf.float32, [None, 10])

        #第一层
        self.W_conv1 = self.weight_variable([5, 5, 1, 32])
        self.b_conv1 = self.bias_variable([32])

        self.x_image = tf.reshape(self.x, [-1, 28, 28, 1])

        self.h_conv1 = tf.nn.relu(self.conv2d(self.x_image, self.W_conv1) + self.b_conv1)
        self.h_pool1 = self.max_pool_2x2(self.h_conv1)

        #第二层
        self.W_conv2 = self.weight_variable([5, 5, 32, 64])
        self.b_conv2 = self.bias_variable([64])

        self.h_conv2 = tf.nn.relu(self.conv2d(self.h_pool1, self.W_conv2) + self.b_conv2)
        self.h_pool2 = self.max_pool_2x2(self.h_conv2)

        self.W_fc1 = self.weight_variable([7 * 7 * 64, 1024])
        self.b_fc1 = self.bias_variable([1024])

        h_pool2_flat = tf.reshape(self.h_pool2, [-1, 7 * 7 * 64])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, self.W_fc1) + self.b_fc1)

        self.keep_prob = tf.placeholder("float")
        self.h_fc1_drop = tf.nn.dropout(h_fc1, self.keep_prob)

        self.W_fc2 = self.weight_variable([1024, 10])
        self.b_fc2 = self.bias_variable([10])

        self.y_conv = tf.nn.softmax(tf.matmul(self.h_fc1_drop, self.W_fc2) + self.b_fc2)

        self.cross_entropy = -tf.reduce_sum(self.y_ * tf.log(self.y_conv))
        self.train_step = tf.train.AdamOptimizer(1e-4).minimize(self.cross_entropy)
        self.correct_prediction = tf.equal(tf.argmax(self.y_conv, 1), tf.argmax(self.y_, 1))
        self.accuracy = tf.reduce_mean(tf.cast(self.correct_prediction, "float"))
        self.prediction = tf.argmax(self.y_conv, 1)

        self.saver = tf.train.Saver()
        self.sess =  tf.Session()
        self.sess.run(tf.global_variables_initializer())
        self.saver.restore(self.sess, path)  # 使用模型，参数和之前的代码保持一致



    def train(self):
        mnist = input_data.read_data_sets('./MNIST_data', one_hot=True)  # MNIST数据集所在路径

        self.x = tf.placeholder(tf.float32, [None, 784])
        self.y_ = tf.placeholder(tf.float32, [None, 10])

        # 第一层
        self.W_conv1 = self.weight_variable([5, 5, 1, 32])
        self.b_conv1 = self.bias_variable([32])

        self.x_image = tf.reshape(self.x, [-1, 28, 28, 1])

        self.h_conv1 = tf.nn.relu(self.conv2d(self.x_image, self.W_conv1) + self.b_conv1)
        self.h_pool1 = self.max_pool_2x2(self.h_conv1)

        # 第二层
        self.W_conv2 = self.weight_variable([5, 5, 32, 64])
        self.b_conv2 = self.bias_variable([64])

        self.h_conv2 = tf.nn.relu(self.conv2d(self.h_pool1, self.W_conv2) + self.b_conv2)
        self.h_pool2 = self.max_pool_2x2(self.h_conv2)

        self.W_fc1 = self.weight_variable([7 * 7 * 64, 1024])
        self.b_fc1 = self.bias_variable([1024])

        h_pool2_flat = tf.reshape(self.h_pool2, [-1, 7 * 7 * 64])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, self.W_fc1) + self.b_fc1)

        self.keep_prob = tf.placeholder("float")
        h_fc1_drop = tf.nn.dropout(h_fc1, self.keep_prob)

        self.W_fc2 = self.weight_variable([1024, 10])
        self.b_fc2 = self.bias_variable([10])

        self.y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, self.W_fc2) + self.b_fc2)

        self.cross_entropy = -tf.reduce_sum(self.y_ * tf.log(self.y_conv))
        self.train_step = tf.train.AdamOptimizer(1e-4).minimize(self.cross_entropy)
        self.correct_prediction = tf.equal(tf.argmax(self.y_conv, 1), tf.argmax(self.y_, 1))
        self.accuracy = tf.reduce_mean(tf.cast(self.correct_prediction, "float"))

        self.saver = tf.train.Saver()

        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            for i in range(4000):
                batch = mnist.train.next_batch(50)
                if i % 100 == 0:
                    train_accuracy = self.accuracy.eval(feed_dict={
                        self.x: batch[0], self.y_: batch[1], self.keep_prob: 1.0})
                    print('step %d, training accuracy %g' % (i, train_accuracy))
                self.train_step.run(feed_dict={self.x: batch[0], self.y_: batch[1], self.keep_prob: 0.5})
            self.saver.save(sess, 'model/model.ckpt') #模型储存位置



    def demo_test_figure():
        """
        *function:demo_test_figure
        功能:加载数字并识别
        """
        test = Figure()
        # test.train()
        test.load_model("model/model.ckpt")
        img = test.read_image("./2.jpg")
        # img.show()
        num = test.find_figure(img)
        print(num)



"""
@@@@例子：
#测试
"""
if __name__ == "__main__":
    Figure.demo_test_figure()
    # test = Figure()
    # while True:
    #     test.train() #训练




