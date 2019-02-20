import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

x = tf.placeholder(tf.float32, shape=(1,1))
y = tf.matmul(x, x)

with tf.Session() as sess:
    rand_array = np.random.rand(1,1)
    print(sess.run(y, feed_dict={x: rand_array}))  # Will succeed.
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





