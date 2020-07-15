import os
import re

from utilities.stringUtils import StringUtils
from sound_and_speech.speechInputRecognitionStreaming import SpeechInputRecognitionStreaming, MicrophoneStreamInputSource
from converse.converse import Converse
from avatar.speech import Speech


class ChatBot(object):

    EXIT_PATTERN = ["jarvisalphaechoexit"]
    WAKE_UP_PATTERN = ["jarvis(wouldyou|please|couldyou)?(please)?talkto(me|us)(please)?",
                       "(wouldyou|please|couldyou)?(please)?talkto(me|us)(please)?jarvis"]
    SHUT_UP_PATTERN = ["jarvis(wouldyou|please|couldyou|)(please)?(shutup|bequiet)(please)?",
                       "(wouldyou|please|couldyou|)(please)?(shutup|bequiet)(please)?jarvis"]

    SAGEMAKER_ENDPOINT = "Your_SageMaker_EndPoint"

    def __init__(self, language_supports):
        self._sentenceListener = SpeechInputRecognitionStreaming(soundInputSource=MicrophoneStreamInputSource.Microphone,
                                                                 language_supports=language_supports)
        self._language_supports = language_supports
        self._converse = Converse(self.SAGEMAKER_ENDPOINT)
        self._speech = Speech(os.path.join(os.getcwd(), "cache"))
        self._responding = True

    def _start_listening(self):
        if not self._responding:
            self._responding = True
            self._speech.speak("Ok. I will start talking. Don't you regret it")
        else:
            self._speech.speak("Yes, I have been listening to you already. Just say something")

    def _stop_listening(self):
        if not self._responding:
            self._speech.speak("Hey, I haven't been listening to you! What make you think so?")
        else:
            self._speech.speak("Ok, I won't listen to you anymore. Bye")
            self._responding = False

    def _regex_match(self, patterns, text):
        text = re.sub(r"[^a-z']+", '', text.lower())

        for pattern in patterns:
            if re.search(pattern, text) is not None:
                return True

        return False

    def _get_sentence(self, sentence, language_code):
        if not StringUtils.is_empty(sentence):
            print(f"Heard: {sentence} {language_code}")

            if self._regex_match(self.EXIT_PATTERN, sentence):
                return True
            elif self._regex_match(self.SHUT_UP_PATTERN, sentence):
                self._stop_listening()
            elif self._regex_match(self.WAKE_UP_PATTERN, sentence):
                self._start_listening()
            elif self._responding:
                reply = self._converse.converse(sentence)

                if reply is None or len(reply) == 0:
                    reply = "I am sorry I don't understand that"

                print(f"Replied: {reply}")

                if not StringUtils.is_empty(reply):
                    self._speech.speak(reply)

        return False

    def start(self):
        self._sentenceListener.listen_forever(callback=self._get_sentence)


chatBot = ChatBot(language_supports=["en-US"])
chatBot.start()
