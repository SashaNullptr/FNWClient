import asyncio
from datetime import datetime
from dateutil import tz
import re

from telethon.sync import TelegramClient
import pandas as pd
from textblob import TextBlob

class ClientAdapter:
    """
    A that extracts information about messages times.
    """

    def __init__(self, api_id, api_hash):

        self.__api_id = api_id
        self.__api_hash = api_hash

        self.__from_zone = tz.tzutc()
        self.__to_zone = tz.tzlocal()

        self.__client = TelegramClient('session_name', api_id, api_hash)
        self.__client.start()

    def __del__(self):
        self.__client.log_out()
        self.__client.disconnect()

    def get_all_message_date_times(self, username,limit=10):
        """
        Get dates and times for all messages exchanged between you and an entity.

        :param str username: Username (or phone number) of entity to get chat history from.
        :param int limit: The number of messages to extract information from.

        :return: Array of dates and times that each messages was sent.
        :rtype: [datetime.datetime]

        >>> ca = ClientAdapter( api_id, api_hash )
        >>> ca.get_all_message_date_times('+11234567891',limit=1)
        >>> ca.get_all_message_date_times('quartz_husky',limit=1)
        """
        return list(map( lambda x: x.date.astimezone(to_zone), self.__client.iter_messages(username,limit=limit)))

    def get_all_message_times(self, username,limit=10):
        """
        Get time stamps (hours, minutes, seconds, microseconds)
        for all messages exchanged between you and an entity.

        :param str username: Username (or phone number) of entity to get chat history from.
        :param int limit: The number of messages to extract information from.

        :return: Array of times that each messages was sent.
        :rtype: [datetime.time]

        >>> ca = ClientAdapter( api_id, api_hash )
        >>> ca.get_all_message_date_times('+11234567891',limit=1)
        >>> ca.get_all_message_date_times('quartz_husky',limit=1)
        """
        return list(map( lambda x: x.date.astimezone(to_zone).time(), self.__client.iter_messages(username,limit=limit)))

    def message_time_histogram(self,username,limit=10):
        """
        Get a time histrogram for all messages exchanged between you and an entity.

        :param str username: Username (or phone number) of entity to get chat history from.
        :param int limit: The number of messages to extract information from.

        >>> from fnw_client import ClientAdapter
        >>> import matplotlib.pyplot as plt
        >>>
        >>> plt.figure()
        >>>
        >>> ca = ClientAdapter( api_id, api_hash )
        >>> time_historgram = ca.message_time_histogram('quartz_husky',limit=100)
        >>> time_histogram.plot(kind='bar')
        >>>
        >>> plt.show()
        """

        times = get_all_message_date_times(username,limit)
        return pd.DataFrame({'hour':times}).groupby(df['hour'].dt.hour).count()

    def get_sentiments(self,username,limit=10):

        def clean_text(text):
            return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())

        def text_sentiment(text):
            return TextBlob(clean_text(text)).sentiment.polarity

        message_iterator = self.__client.iter_messages(username,limit=limit)
        sentiments = list(map( lambda x: text_sentiment(x.text), message_iterator))
