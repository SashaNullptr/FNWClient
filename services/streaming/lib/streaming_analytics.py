import asyncio
from datetime import datetime
from dateutil import tz
import re

from telethon import TelegramClient, events, utils
from textblob import TextBlob

from prometheus_client import Gauge, Histogram

import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',level=logging.WARNING)


class StreamingAnalytics:
    """
    Log information about events as they happen
    """

    def __init__(self, api_id, api_hash, session):

        self.__api_id = api_id
        self.__api_hash = api_hash
        self.__session = session

        self.__from_zone = tz.tzutc()
        self.__to_zone = tz.tzlocal()

        self.__sentiment_gauge = Gauge(
            'sentiment', 'Sentiment score',
            ["user"]
        )

        self.__contact_times = Histogram(
            'message_end_times', 'Message send times',
            ["user"]
        )

    def init_client(self):

        with TelegramClient(StringSession(self.__session), self.__api_id, self.__api_hash) as client:

            client.add_event_handler(self.log_sentiment, events.NewMessage())
            client.add_event_handler(self.log_time, events.NewMessage())
            # client.loop.run_until_complete(client(GetStateRequest()))
            client.run_until_disconnected()

    async def log_sentiment(self, event):
        """

        Log sentiment of currently received message to a Prometheus gauge.

        If the current message contains no valid text, do nothing.

        :param event: a new message.
        """

        def text_sentiment(text):

            def clean_text(text):
                return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())

            cln_text = clean_text(text)
            return None if not cln_text else TextBlob(cln_text).sentiment.polarity

        sentiment = text_sentiment(event.raw_text)

        logging.warning("Got the following message: \"" + event.raw_text + "\" with sentiment score " + str(sentiment))

        if sentiment:

            sender = await event.get_sender()
            user =  utils.get_display_name(sender)
            self.__sentiment_gauge.labels(user).set(sentiment)

    async def log_time(self, event):
        """

        Log time that a current message was received to a Prometheus Historgram.

        :param event: a new message.
        """
        sender = await event.get_sender()
        user =  utils.get_display_name(sender)

        message = event.message

        time = message.date.astimezone(self.__to_zone).time().hour

        logging.warning("Got the following message: \"" + event.raw_text + "\" at time " + str(time))

        self.__contact_times.labels(user).observe(time)

    @staticmethod
    async def __extract_sender_name(self, event):
        sender = await event.get_sender()
        return utils.get_display_name(sender)

    @staticmethod
    async def __extract_time_sent(self, event):
        message = await event.message()
        return message.astimezone(self.__to_zone).time()
