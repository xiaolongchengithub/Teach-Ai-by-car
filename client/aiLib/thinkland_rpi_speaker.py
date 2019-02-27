import pyttsx3
import pyaudio
import time
import threading
import wave

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

# class Recorder():
#     def __init__(self, chunk=1024, channels=1, rate=64000):
#         self.CHUNK = chunk
#         self.FORMAT = pyaudio.paInt16
#         self.CHANNELS = channels
#         self.RATE = rate
#         self._running = True
#         self._frames = []
#
#     def start(self):
#         threading._start_new_thread(self.__recording, ())
#
#     def __recording(self):
#         self._running = True
#         self._frames = []
#         p = pyaudio.PyAudio()
#         stream = p.open(format=self.FORMAT,
#                         channels=self.CHANNELS,
#                         rate=self.RATE,
#                         input=True,
#                         frames_per_buffer=self.CHUNK)
#         while (self._running):
#             data = stream.read(self.CHUNK)
#             self._frames.append(data)
#
#         stream.stop_stream()
#         stream.close()
#         p.terminate()
#
#     def stop(self):
#         self._running = False
#
#     def save(self, filename):
#
#         p = pyaudio.PyAudio()
#         if not filename.endswith(".wav"):
#             filename = filename + ".wav"
#         wf = wave.open(filename, 'wb')
#         wf.setnchannels(self.CHANNELS)
#         wf.setsampwidth(p.get_sample_size(self.FORMAT))
#         wf.setframerate(self.RATE)
#         wf.writeframes(b''.join(self._frames))
#         wf.close()
#         print("Saved")
#
#
#
