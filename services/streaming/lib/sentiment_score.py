from os import getenv
from pathlib import Path

from services.streaming.lib.text_blob_sentiment import text_sentiment
from services.streaming.lib.flair_sentiment import FlairTextSentiment

import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',level=logging.DEBUG)
logger = logging.getLogger(__name__)


class SentimentScoreModel:

    def __init__(self):
        model_location = getenv('SENTIMENT_MODEL', "/opt/models/sentiment/final-model.pt")
        model_path = Path(model_location)

        if not model_path.exists():
            logger.warning("Couldn't find Flair model at " + str(model_path) + " using TextBlob instead.")
            self.__score_function = text_sentiment
        else:
            logger.warning("Using Flair to compute sentiment score with model loaded from " + str(model_path) )
            self.__model = FlairTextSentiment(model_path)
            self.__score_function = self.__model.text_sentiment

    def sentiment_score(self, raw_text):
        return self.__score_function(raw_text)