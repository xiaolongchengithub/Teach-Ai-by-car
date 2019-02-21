import numpy as np
import tensorflow as tf

#最近邻算法，此代码实现类似1-NN
#导入输入数据MNIST


# from tensorflow.examples.tutorials.mnist import input_data
# mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)


x = np.array([[12,3,34,55],[2,2,2,2],[2,32,1,5]])
print(type(x))
x1 = x[1,:]
y = x - x1
print(x1)
print(y)
print(np.argmin(y,1))
#
# # #这个例子限制了样本的数目
# Xtr, Ytr = mnist.train.next_batch(1000) #1000 条候选样本，测试样本跟候选样本比较，得到最近的K个样本，然后k个样本的标签大多数为某类，测试样本就为某类
# Xte, Yte = mnist.test.next_batch(2) #200 条测试样本
# print(Yte)
# print(Xte)
# cross = Xte-Xte[1:]
# print(Xte)
#
# # tf Graph Input，占位符，用来feed数据
# xtr = tf.placeholder("float", [None, 784])
# xte = tf.placeholder("float", [784])
#
#
# # 最近邻计算距离使用 L1 距离
# # 计算L1距离
# distance = tf.reduce_sum(tf.abs(tf.add(xtr, tf.negative(xte))), reduction_indices=1)
# # 预测: 获取离测试样本具有最小L1距离的样本(1-NN），此样本的类别作为test样本的类别
# pred = tf.arg_min(distance, 0)
#
#
# accuracy = 0.
#
#
# # 初始化图
# init = tf.global_variables_initializer()
#
# # 发布图
# with tf.Session() as sess:
#     sess.run(init)
#
#     #循环测试集
#     for i in range(len(Xte)):
#         # Get nearest neighbor
#         nn_index = sess.run(pred, feed_dict={xtr: Xtr, xte: Xte[i, :]})  #每次循环feed数据，候选Xtr全部，测试集Xte一次循环输入一条
#         # 获得与测试样本最近样本的类别，计算与真实类别的误差
#         print("Test", i, "Prediction:", np.argmax(Ytr[nn_index]), \
#               "True Class:", np.argmax(Yte[i]))
#         # 计算误差率
#         if np.argmax(Ytr[nn_index]) == np.argmax(Yte[i]):
#             accuracy += 1. / len(Xte)
#     print("Done!")
#     print("Accuracy:", accuracy)



# import tensorflow as tf
# import numpy as np
# import matplotlib.pyplot as plt
#
# x = tf.placeholder(tf.float32, shape=(1,1))
# y = tf.matmul(x, x)
#
# with tf.Session() as sess:
#     rand_array = np.random.rand(1,1)
#     print(sess.run(y, feed_dict={x: rand_array}))  # Will succeed.
# import time
#
# trX = np.random.rand(10)
#
# tr = trX*2 + 3.33
#
# w = tf.Variable(1.0)
#
# b = tf.Variable(4.0)
#
# y = trX*w + b
#
# y_cross = tf.reduce_mean(tf.square(y-tr))
#
# optmiszer = tf.train.GradientDescentOptimizer(0.01)
#
# train = optmiszer.minimize(y_cross)
#
# init = tf.global_variables_initializer()
#
# sess = tf.Session()
#
# sess.run(init)
# plt.figure()
# axle = plt.subplot(111)
# axle.plot(trX, tr)
# plt.ion()
# plt.show()
# for step in range(6000):
#         sess.run(train)
#         #画出预测数据
#         if(step%10 == 0):
#             print(step ,sess.run([w,b]))
#             w1 = sess.run(w)
#             b1 = sess.run(b)
#             line = axle.plot((trX),((trX)*w1+b1))
#             plt.ion()
#             plt.show()
#             plt.pause(0.1)
#             axle.lines.remove(line[0])
#
# plt.show()
#
#
# sess.close()

# import numpy as np
# import tensorflow as tf
#
# # create data
# x_data = np.random.rand(100).astype(np.float32)
# y_data = x_data * 0.1 + 5.0
#
# # create tensorflow structure start
# Weights = tf.Variable(tf.random_uniform([1], -1.0, 1.0))
# biases = tf.Variable(tf.zeros([1]))
#
# y = Weights * x_data + biases
#
# loss = tf.reduce_mean(tf.square(y - y_data))
# optimizer = tf.train.GradientDescentOptimizer(0.5)
# train = optimizer.minimize(loss)
#
# init = tf.initialize_all_variables()
# # create tensorflow structure end
#
# ses = tf.Session()
# ses.run(init)
#
# for step in range(1000):
#     if step % 20 == 0:
#         print(step, ses.run(Weights), ses.run(biases))





