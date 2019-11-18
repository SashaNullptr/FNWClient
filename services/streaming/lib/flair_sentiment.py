import re

# Some of flair's dependencies *require* Python 3.6
from flair.data import Sentence
from flair.models import TextClassifier

from services.streaming.lib.clean_text import clean_text

# en-sentiment model is hosted at
# https://s3.eu-central-1.amazonaws.com/alan-nlp/resources/models-v0.4/classy-imdb-en-rnn-cuda%3A0/imdb-v0.4.pt
# If this model isn't loaded in advance it will take 5-ish minutes to download
# Model is saved in ~/.flair/models by default


class FlairTextSentiment:

    def __init__(self):
        self.__model = TextClassifier.load('en-sentiment')

    # By default label objects represent a score as either value:<str> score:<float>
    # where value is either "POSITIVE" or "NEGATIVE"
    # We need to convert this isn't something less stupid.
    def __sentiment(self, text):

        sentence = Sentence(text)
        self.__model.predict(sentence)

        score = sentence.labels[0].score

        value = sentence.labels[0].value
        sign = 1 if (value == "POSITIVE") else -1

        return sign*score

    def text_sentiment(self, text):

        cln_text = clean_text(text)

        return None if not cln_text else self.__sentiment(cln_text)