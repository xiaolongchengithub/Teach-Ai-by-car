"""
    speaker类可以将文本转化为语音
"""
import pyttsx3


class Speaker():
    """
    现在只是针对windows
    """

    def __init__(self):
        """初始化类型,初始化
        """

        self.speaker = pyttsx3.init()

    def say(self, word):
        """将文本转化为语音

        Parameters
        ------------
        * word : string
            - 要说的话

        Returns
        -------
        * None
        """
        self.speaker.say(word)
        self.speaker.runAndWait()

    @staticmethod
    def demo_say():
        """演示demo
        """
        test = Speaker()
        test.say("hello")
        test.say("hello")
        test.say("hello")


if __name__ == "__main__":
    Speaker.demo_say()
