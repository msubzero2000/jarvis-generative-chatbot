import os


class StringUtils(object):

    @classmethod
    def is_empty(cls, text):
        return text is None or len(text) == 0
