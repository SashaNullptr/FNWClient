from textblob import TextBlob
from services.streaming.lib.clean_text import clean_text


def text_sentiment(text):

    cln_text = clean_text(text)
    return None if not cln_text else TextBlob(cln_text).sentiment.polarity