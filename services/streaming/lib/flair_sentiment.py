import re
from pathlib import Path

# Some of flair's dependencies *require* Python 3.6
from flair.data import Sentence
from flair.models import TextClassifier

from services.streaming.lib.clean_text import clean_text

# en-sentiment model is hosted at
# https://s3.eu-central-1.amazonaws.com/alan-nlp/resources/models-v0.4/classy-imdb-en-rnn-cuda%3A0/imdb-v0.4.pt
# If this model isn't loaded in advance it will take 5-ish minutes to download
# Model is saved in ~/.flair/models by default
import flair, torch


class FlairTextSentiment:

    def __init__(self, model_location):
        model_path = Path(model_location)

        if not model_path.exists():
            raise FileNotFoundError( "Could Flair model at " + str(model_path) )

        self.__model = TextClassifier.load(model_path)

        # Our image doesn't currently support GPU passthrough--so don't bother trying.
        flair.device = torch.device('cpu')

    # By default label objects represent a score as either value:<str> score:<float>
    # where value is either "POSITIVE" or "NEGATIVE"
    # We need to convert this isn't something less stupid.
    def __sentiment(self, text):

        sentence = Sentence(text)
        self.__model.predict(sentence)

        score = sentence.labels[0].score # Confidence score
        value = int(sentence.labels[0].value) # Sentiment value

        # Value labels will be on the following scale
        # 1: Strongly Negative
        # 2: Weakly Negative
        # 3: Neutral
        # 4: Weakly Positive
        # 5: Strongly Positive
        # We'll convert to a [1,-1] score for simplicity

        sentiment = 2*((value-1)/4 - 0.5)

        return sentiment

    def text_sentiment(self, text):

        cln_text = clean_text(text)

        return None if not cln_text else self.__sentiment(cln_text)