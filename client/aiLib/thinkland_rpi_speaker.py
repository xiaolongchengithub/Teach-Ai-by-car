
import pyttsx3
import time
import threading

"""
实现功能把文本转换为语音的功能，现在只能在windows上调用
"""

class Speaker():
    """
    现在只是针对windows
    """
    def __init__(self):
        """
        ________
        功能：初始化类型,初始化（现在的初始化只是针对windows）
        ________
        """

        self.speaker = pyttsx3.init()

    def say(self , word):
        """
        *function:speak
        功能：控制LED灯的开关
        ________
        Parameters
        * word : string
        - 要说的话
        ————
        Returns
        -------
        * None
        """
        self.speaker.say(word)
        self.speaker.runAndWait()

    @staticmethod
    def demo_say():
        """
        @@@@例子：
        #利展示
        """
        test = Speaker()
        test.say("hello")
        test.say("hello")
        test.say("hello")

"""
@@@@例子：
#利用windows库实现朗读功能
"""
if __name__ == "__main__":
    Speaker.demo_say()
