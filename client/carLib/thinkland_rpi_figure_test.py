from PIL import Image, ImageFilter
import tensorflow as tf
import matplotlib.pyplot as plt

"""
模块功能：识别图片数字，模型的目录为当前目录
"""

class Figure():
    def __init__(self):
        print('figure init')
        self.load_model()

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

    def find_figure(self):
        im = Image.open('D:/3.jpg') #读取的图片所在路径，注意是28*28像素
        im = im.resize((28, 28), Image.ANTIALIAS)
        # plt.imshow(im)  #显示需要识别的图片
        # plt.show()
        im = im.convert('L')
        tv = list(im.getdata())
        tva = [(255-x)*1.0/255.0 for x in tv]
        result = tva
        predint = self.prediction.eval(feed_dict={self.x: [result], self.keep_prob: 1.0}, session=self.sess)
        print('识别结果:')
        print(predint[0])
        return predint[0]

    def load_model(self):
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
        h_fc1_drop = tf.nn.dropout(h_fc1, self.keep_prob)

        self.W_fc2 = self.weight_variable([1024, 10])
        self.b_fc2 = self.bias_variable([10])

        self.y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, self.W_fc2) + self.b_fc2)

        self.cross_entropy = -tf.reduce_sum(self.y_ * tf.log(self.y_conv))
        self.train_step = tf.train.AdamOptimizer(1e-4).minimize(self.cross_entropy)
        self.correct_prediction = tf.equal(tf.argmax(self.y_conv, 1), tf.argmax(self.y_, 1))
        self.accuracy = tf.reduce_mean(tf.cast(self.correct_prediction, "float"))

        self.saver = tf.train.Saver()

        self.sess =  tf.Session()
        self.sess.run(tf.global_variables_initializer())
        self.saver.restore(self.sess, "model/model.ckpt")  # 使用模型，参数和之前的代码保持一致
        self.prediction = tf.argmax(self.y_conv, 1)


test  =  Figure()
while True:
    test.find_figure()




