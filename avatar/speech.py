import os
import boto3
import hashlib
import time
import playsound

from utilities.fileSearch import FileSearch


class Speech(object):
    _YOUR_AWS_KEY = "YOUR_AWS_KEY_HERE"
    _YOUR_AWS_SECRET = "YOUR_AWS_SECRET_HERE"

    def __init__(self, audioFolder):
        self._audioFolder = audioFolder
        audioFilePathList = FileSearch.collectFilesEndsWithNameRecursively(".ogg", audioFolder)

        self._cache = {}
        for path in audioFilePathList:
            fileName = path.split("/")[-1].split(".")[0]
            self._cache[fileName] = path

        self._pollyClient = boto3.Session(
                        region_name='ap-southeast-2').client('polly')

    def speak(self, text):
        hashObject = hashlib.sha1(text.encode())
        hash = hashObject.hexdigest()

        if hash in self._cache:
            audioFilePath = self._cache[hash]
        else:
            audioFilePath = self._tts(text, hash)

        self._cache[hash] = audioFilePath
        playsound.playsound(audioFilePath, block=True)

    def isSpeaking(self):
        return self._audio.isPlaying()

    def isAfterSpeaking(self):
        return self._audio.isAfterPlaying()

    def _tts(self, text, hash):
        response = self._pollyClient.synthesize_speech(VoiceId='Ivy',
                        OutputFormat='mp3',
                        Text = text)
        filePath = os.path.join(self._audioFolder, "{0}.mp3".format(hash))
        file = open(filePath, 'wb')
        file.write(response['AudioStream'].read())
        file.close()

        return filePath