from datetime import datetime
from dateutil import tz
import re

from telethon import TelegramClient, events
from textblob import TextBlob

from prometheus_client import Gauge, Histogram


class StreamingAnalytics:
    """
    Log information about events as they happen
    """

    def __init__(self, api_id, api_hash):

        self.__api_id = api_id
        self.__api_hash = api_hash

        self.__from_zone = tz.tzutc()
        self.__to_zone = tz.tzlocal()

        self.__client = TelegramClient('session_name', api_id, api_hash)

        self.__client.add_event_handler(self.log_sentiment, events.NewMessage())
        self.__client.add_event_handler(self.log_time, events.NewMessage())

        self.__sentiment_gauge = Gauge(
            'sentiment', 'Sentiment score',
            ['app_name', 'endpoint']
        )

        self.__contact_times = Histogram(
            'message_end_times', 'Message send times',
            ['app_name', 'endpoint']
        )

        self.__client.start()

    def __del__(self):
        self.__client.log_out()
        self.__client.disconnect()

    def log_sentiment(self, event: events.NewMessage):
        sentiment = self.__text_sentiment(event.raw_text)
        if sentiment:
            self.__sentiment_gauge.set(sentiment)

    def log_time(self, event: events.common):
        pass

    def __text_sentiment(self,text):

        def clean_text(self,text):
            return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())

        cln_text = clean_text(text)
        return None if not cln_text else TextBlob(cln_text).sentiment.polarity
