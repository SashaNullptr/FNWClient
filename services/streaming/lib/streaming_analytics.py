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

    def __init__(self, api_id, api_hash):

        self.__api_id = api_id
        self.__api_hash = api_hash

        self.__from_zone = tz.tzutc()
        self.__to_zone = tz.tzlocal()

        # self.__client.add_event_handler(self.log_time, events.NewMessage())

        self.__sentiment_gauge = Gauge(
            'sentiment', 'Sentiment score',
        )

        self.__contact_times = Histogram(
            'message_end_times', 'Message send times',
        )

        self.__client =  TelegramClient('streaming_analytics', api_id, api_hash)

    def __del__(self):

        self.__client.disconnect()

        # with TelegramClient('streaming_analytics', api_id, api_hash) as client:
        #     client.add_event_handler(self.log_sentiment, events.NewMessage())
        #     client.run_until_disconnected()
    def send_code_to_number(self, phone):
        """
        Send login code to a phone number.

        :param phone: Phone number in international format, e.g "+12345678910"
        """

        async def send_code(phone_num):
            await self.__client.connect()
            await self.__client.send_code_request(phone_num)
            await self.__client.disconnect()

        self.__client.loop.run_until_complete(send_code(phone))

    def authenticate_session(self, phone, code):
        """
        Authenticate current client session.

        :param phone: Phone number in international format, e.g "+12345678910"
        :param code: Six digit code received from Telegram e.g. "123456"
        """

        async def auth_sess(phone_num, code_recv):

            await self.__client.connect()
            await self.__client.sign_in(phone_num,code_recv)
            await self.__client.disconnect()

        self.__client.loop.run_until_complete(auth_sess(phone,code))

    def run(self):

        async def run_client():
            await self.__client.connect()
            await self.__client.add_event_handler(self.log_sentiment, events.NewMessage())

        if self.__client.loop.run_until_complete(self.__client.is_user_authorized()):
            self.__client.loop.run_until_complete(run_client())
            self.__client.run_until_disconnected()
        # with self.__client as client:
        #     client.add_event_handler(self.log_sentiment, events.NewMessage())
        #     client.run_until_disconnected()

    async def log_sentiment(self, event: events.NewMessage):
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
        logging.warning("Got the following message:", event.raw_text, " with sentiment score ", sentiment)
        if sentiment:
            self.__sentiment_gauge.set(sentiment)

    async def log_time(self, event: events.NewMessage):
        """

        Log time that a current message was received to a Prometheus Historgram.

        :param event: a new message.
        """
        pass

    async def __extract_sender_name(self,event):
        sender = await event.get_sender()
        return utils.get_display_name(sender)
