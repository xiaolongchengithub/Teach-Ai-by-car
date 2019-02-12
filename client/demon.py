# import tensorflow
import  client as  test
import  time

test.init(("172.16.10.227", 12347),("172.16.10.227"),"172.16.10.223" )

control = test.control
img = test.camera

# angle = [45,90,135,90]
# control.controlCameraAngle(18, 90)
# time.sleep(5)

# while True:
#     ret = img.findLine()
#     x = ret[0]
#     print(x)
#     if 220 < x < 420:
#         control.run(1,0.5)
#     elif 0< x <= 220:
#         control.left(0.5, 0.1)
#     elif x >= 420:
#         control.right(0.5,0.1)
#     else:
#         control.brake(5)
    # time.sleep(0.01)


# while True:
#     for ag in angle:
#         control.controlCameraAngle(45, ag,1)
#
# for num in range(10,26):
#     ret = img.imgTest('cup')
# for num in range(10,26):
#     ret = img.imgTest('cup')
#     if ret:
#         control.run(10, 1)
#         break
#     else:
#         control.spinLeft(10, 0.25)
#     time.sleep(2)
# ##################################################################################run and look for
#     FindObject = False
#     while FindObject == False:
#
#         control.controlCameraAngle(20, 90)
#         ret = img.imgTest('cup')
#         if ret == True:
#             break
#
#         control.controlCameraAngle(20, 60)
#         ret = img.imgTest('cup')
#
#         if ret == True:
#             control.spinRight(10,0.5)
#             control.controlCameraAngle(20, 90)
#             break
#
#         control.controlCameraAngle(20, 120)
#         ret = img.imgTest('cup')
#         if ret == True:
#             control.spinLeft(10,0.5)
#             control.controlCameraAngle(20, 90)
#             break
#
#
#         control.controlCameraAngle(45, 45)
#         ret = img.imgTest('cup')
#         if ret == True:
#             control.spinRight(10, 0.5)
#
#
#         control.controlCameraAngle(45, 135)
#         ret = img.imgTest('cup')
#         if ret == True:
#             control.spinLeft(10, 0.5)
#
#         control.controlCameraAngle(45, 90)
#         ret = img.imgTest('cup')
#         if ret == True:
#             control.run(10, 0.5)
#
#         control.run(10,1.5)
#     while True:
#         time.sleep(0.5)

# import speech_recognition as sr
#
# # obtain audio from the microphone
# r = sr.Recognizer()
# with sr.Microphone() as source:
#     print("Say something!")
#     audio = r.listen(source)
#
# # recognize speech using Google Cloud Speech
# GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""INSERT THE CONTENTS OF THE GOOGLE CLOUD SPEECH JSON CREDENTIALS FILE HERE"""
# try:
#     print("Google Cloud Speech thinks you said " + r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
# except sr.UnknownValueError:
#     print("Google Cloud Speech could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from Google Cloud Speech service; {0}".format(e))
#
# # recognize speech using Wit.ai
# WIT_AI_KEY = "INSERT WIT.AI API KEY HERE"  # Wit.ai keys are 32-character uppercase alphanumeric strings
# try:
#     print("Wit.ai thinks you said " + r.recognize_wit(audio, key=WIT_AI_KEY))
# except sr.UnknownValueError:
#     print("Wit.ai could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from Wit.ai service; {0}".format(e))
#
# # recognize speech using Microsoft Bing Voice Recognition
# BING_KEY = "INSERT BING API KEY HERE"  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
# try:
#     print("Microsoft Bing Voice Recognition thinks you said " + r.recognize_bing(audio, key=BING_KEY))
# except sr.UnknownValueError:
#     print("Microsoft Bing Voice Recognition could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
#
# # recognize speech using Houndify
# HOUNDIFY_CLIENT_ID = "INSERT HOUNDIFY CLIENT ID HERE"  # Houndify client IDs are Base64-encoded strings
# HOUNDIFY_CLIENT_KEY = "INSERT HOUNDIFY CLIENT KEY HERE"  # Houndify client keys are Base64-encoded strings
# try:
#     print("Houndify thinks you said " + r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY))
# except sr.UnknownValueError:
#     print("Houndify could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from Houndify service; {0}".format(e))
#
# # recognize speech using IBM Speech to Text
# IBM_USERNAME = "INSERT IBM SPEECH TO TEXT USERNAME HERE"  # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
# IBM_PASSWORD = "INSERT IBM SPEECH TO TEXT PASSWORD HERE"  # IBM Speech to Text passwords are mixed-case alphanumeric strings
# try:
#     print("IBM Speech to Text thinks you said " + r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD))
# except sr.UnknownValueError:
#     print("IBM Speech to Text could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from IBM Speech to Text service; {0}".format(e))
# import speech
# import win32api
# import os
# import sys
# import time
# import win32con
# command1 = {'关机': 'shutdown -s -t 1',
#              '重启': 'shutdown -r',
#              '关闭浏览器': 'taskkill /F /IM chrome.exe',
#              'google一下': 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
#              '关闭QQ': 'taskkill /F /IM QQ.exe',
#              '关闭wifi': 'taskkill /F /IM kwifi.exe',
#              '关闭音乐': 'taskkill /F /IM cloudmusic.exe',
#              '打开音乐': 'D:\\网易云音乐\\CloudMusic\\cloudmusic.exe',
#              '放首歌': 'D:\\网易云音乐\\CloudMusic\\cloudmusic.exe',
#              '打开摄像头': 'D:\\Python源码\\摄像头监控.py',
#              '打开监控': 'D:\\Python源码\\winSpyon.py',
#              '打开QQ': 'D:\\腾讯QQ\\Bin\\QQ.exe',
#              '开启wifi': 'D:\\Chrome\\kwifi\\kwifi.exe',
#              '连接校园网': 'C:\\Drcom\\DrUpdateClient\\DrMain.exe',
#              '打开ss': 'D:\\代理服务器\\Shadowsocks-win-dotnet4.0-2.3\\Shadowsocks.exe',
#              '打开pycharm': 'D:\\PyCharm\\PyCharm 4.0.4\\bin\\pycharm64.exe',
#              '关闭pycharm': 'taskkill /F /IM pycharm.exe',
#              '打开everything': 'D:\\Chrome\\Everything\\Everything.exe',
#              '关闭everything': 'taskkill /F /IM everything.exe',
#               }
# speech.say('语音识别已开启 ')
# while True:
#     phrase = speech.input()
#     if phrase in command1.keys():
#         speech.say('即将为您%s' %phrase)
#         os.system(command1[phrase])
#         speech.say('任务已完成！')
#         if phrase == '放首歌':
#             speech.say('30秒后将播放音乐！')
#             time.sleep(35)
#             win32api.keybd_event(17, 0, 0, 0)
#             win32api.keybd_event(18, 0, 0, 0)
#             win32api.keybd_event(32, 0, 0, 0)
#             win32api.keybd_event(32, 0, win32con.KEYEVENTF_KEYUP, 0)
#             win32api.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)
#             win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
#     if phrase == '退出程序':
#          speech.say('已退出程序，感谢使用！')
#          sys.exit()
