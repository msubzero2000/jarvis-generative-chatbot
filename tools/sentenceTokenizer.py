import nltk.data

nltk.download('punkt')
nltk.download('stopwords')

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


class SentenceTokeniser(object):
    def __init__(self):
        pass

    def tokenizeSentence(self, text):
        sentences = tokenizer.tokenize(text)

        return sentences
