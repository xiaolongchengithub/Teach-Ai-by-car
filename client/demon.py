# import threading
# import sys
# import os
# import time
#
# from urllib import URLError
# from urllib import urlencode
# import urllib
# import numpy as np
# import urllib.request
# import urllib.URL
#
# if sys.platform == "win32":
#     timer = time.clock
# else:
#     timer = time.time
#
# import httplib
# from TestServer import models
# from TestServer.views import make_report
# import time
# import hashlib
# import threadpool
# import base64
# import json
# import requests
# from AsrTest.views.tools import wer
#
#
# class AliApi(object):
#     def __init__(self, audiolistFile, thread_sum=10):
#         self.audiolistFile = audiolistFile
#         self.appKey = '***'
#         self.token = '***'
#         # 服务请求地址
#         self.url = 'http://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/asr'
#         # 音频文件
#         self.audioFile = '/path/to/nls-sample-16k.wav'
#         self.format = 'pcm'
#         self.sampleRate = 16000
#         self.enablePunctuationPrediction = True
#         self.enableInverseTextNormalization = True
#         self.enableVoiceDetection = False
#         self.request = self.url + '?appkey=' + self.appKey
#         self.request = self.request + '&format=' + self.format
#         self.request = self.request + '&sample_rate=' + str(self.sampleRate)
#         if self.enablePunctuationPrediction:
#             self.request = self.request + '&enable_punctuation_prediction=' + 'true'
#         if self.enableInverseTextNormalization:
#             self.request = self.request + '&enable_inverse_text_normalization=' + 'true'
#         if self.enableVoiceDetection:
#             self.request = self.request + '&enable_voice_detection=' + 'true'
#
#         with open(self.audiolistFile, "r") as audiolistFile:
#             audio_list = audiolistFile.readlines()
#         # 确定总线程数
#         if thread_sum > 10:
#             thread_sum = 10
#         pool = threadpool.ThreadPool(thread_sum)
#         self.aliof = open("ali.txt", "w")
#         requests = threadpool.makeRequests(self.run, audio_list)
#         [pool.putRequest(req) for req in requests]
#         pool.wait()
#         self.aliof.close()
#
#     def run(self, audio_file):
#         audio_file = audio_file.replace("\n", "").replace("\r", "")
#         with open(audio_file, mode='rb') as f:
#             audioContent = f.read()
#         host = 'nls-gateway.cn-shanghai.aliyuncs.com'
#         # 设置HTTP请求头部
#         httpHeaders = {
#             'X-NLS-Token': self.token,
#             'Content-type': 'application/octet-stream',
#             'Content-Length': len(audioContent)
#         }
#         conn = httplib.HTTPConnection(host)
#         conn.request(method='POST', url=self.request, body=audioContent, headers=httpHeaders)
#         response = conn.getresponse()
#         print(response.status, response.reason)
#         body = response.read()
#         try:
#             print('Recognize response is:')
#             body = json.loads(body)
#             print(body)
#             status = body['status']
#             if status == 20000000:
#                 result = body['result']
#                 print('[Ali]' + ":" + result)
#                 self.aliof.write(nosignal(audio_file.split(".")[0] + "\t" + result.encode('utf-8') + '\n'))
#             else:
#                 print('Recognizer failed!')
#         except ValueError:
#             print('The response is not json format string')
#         conn.close()
#


import json
import time
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

def fileTrans(akId, akSecret, appKey, fileLink) :
    REGION_ID = "cn-shanghai"
    PRODUCT = "nls-filetrans"
    DOMAIN = "filetrans.cn-shanghai.aliyuncs.com"
    API_VERSION = "2018-08-17"
    POST_REQUEST_ACTION = "SubmitTask"
    GET_REQUEST_ACTION = "GetTaskResult"

    KEY_APP_KEY = "app_key"
    KEY_FILE_LINK = "file_link"
    KEY_TASK = "Task"
    KEY_TASK_ID = "TaskId"
    KEY_STATUS_TEXT = "StatusText"

    # 创建AcsClient实例
    client = AcsClient(akId, akSecret, REGION_ID)

    # 创建提交录音文件识别请求，并设置请求参数
    postRequest = CommonRequest()
    postRequest.set_domain(DOMAIN)
    postRequest.set_version(API_VERSION)
    postRequest.set_product(PRODUCT)
    postRequest.set_action_name(POST_REQUEST_ACTION)
    postRequest.set_method('POST')

    task = {KEY_APP_KEY : appKey, KEY_FILE_LINK : fileLink}
    task = json.dumps(task)
    postRequest.add_body_params(KEY_TASK, task)

    try :
        # 提交录音文件识别请求，处理服务端返回的响应
        postResponse = client.do_action_with_exception(postRequest)
        print(postResponse)
        print(type(postResponse))
        data = str(postResponse, encoding="utf-8")
        print(data)
        print(type(data))
        postResponse = json.loads(data)
        print (postResponse)

        # 获取录音文件识别请求任务的ID，以供识别结果查询使用
        taskId = ""
        statusText = postResponse[KEY_STATUS_TEXT]
        if statusText == "SUCCESS" :
            print ("录音文件识别请求成功响应！")
            taskId = postResponse[KEY_TASK_ID]
        else :
            print ("录音文件识别请求失败！")
            return
    except ServerException as e:
        print (e)
    except ClientException as e:
        print (e)


    # 创建识别结果查询请求，设置查询参数为任务ID
    getRequest = CommonRequest()
    getRequest.set_domain(DOMAIN)
    getRequest.set_version(API_VERSION)
    getRequest.set_product(PRODUCT)
    getRequest.set_action_name(GET_REQUEST_ACTION)
    getRequest.set_method('GET')

    getRequest.add_query_param(KEY_TASK_ID, taskId)

    # 提交录音文件识别结果查询请求
    # 以轮询的方式进行识别结果的查询，直到服务端返回的状态描述符为"SUCCESS"、"SUCCESS_WITH_NO_VALID_FRAGMENT"，
    # 或者为错误描述，则结束轮询。
    statusText = ""
    while True :
        try :
            getResponse = client.do_action_with_exception(getRequest)
            getdata = str(getResponse, encoding="utf-8")
            getResponse = json.loads(getdata)
            print(111111111111111111111)
            print (getResponse)

            statusText = getResponse[KEY_STATUS_TEXT]
            if statusText == "RUNNING" or statusText == "QUEUEING" :
                # 继续轮询
                time.sleep(3)
            else :
                # 退出轮询
                break
        except ServerException as e:
            print (e)
        except ClientException as e:
            print (e)


    if statusText == "SUCCESS" or statusText == "SUCCESS_WITH_NO_VALID_FRAGMENT" :
        print ("录音文件识别成功！")
        print(getResponse['Result']['Sentences'][0]['Text'])
    else :
        print ("录音文件识别失败！")

    return




accessKeyId = "LTAIGOt9PSGiZ0oH"
accessKeySecret = "rYYIv21ubR2ksfNs24NOU8N6uG6ARc"
appKey = "rMBBTXQL8Qr1BMMu"
fileLink = "D://11.wav"

# 执行录音文件识别
fileTrans(accessKeyId, accessKeySecret, appKey, fileLink)

# import numpy as np
# import tensorflow as tf
# import json
#
# #最近邻算法，此代码实现类似1-NN
# #导入输入数据MNIST
#
#
# import pyttsx3
#
#
#
# engine = pyttsx3.init()
# engine.say('hello world')
# engine.say('你好吗')
# engine.runAndWait()
#
#
# model={} #数据
# model["Ip"] = "192.16.170.29"
# with open("./test.json",'w',encoding='utf-8') as json_file:
#     json.dump(model,json_file,ensure_ascii=False)
#
# read={} #存放读取的数据
# with open("./test.json",'r',encoding='utf-8') as json_file:
#     read=json.load(json_file)
#
# print(read['Ip'])

# from tensorflow.examples.tutorials.mnist import input_data
# mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)


# def test():
#     print(22)
#     while True:
#         input = (np.random.rand(2)-0.5)*20
#         output= input[1]>input[0]
#         yield input,output.astype(np.float32)
#
# print(11)
# test()
# print(33)
# x = np.array([[12,3,34,55],[2,2,2,2],[2,32,1,5]])
# print(type(x))
# x1 = x[1,:]
# y = x - x1
# print(x1)
# print(y)
# print(np.argmin(y,1))
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





