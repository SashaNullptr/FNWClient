from telethon.sync import TelegramClient
import pandas as pd
import asyncio

from datetime import datetime
from dateutil import tz

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

    def plot_message_times(self,username,limit=10):
        """
        Get a time histrogram for all messages exchanged between you and an entity.

        :param str username: Username (or phone number) of entity to get chat history from.
        :param int limit: The number of messages to extract information from.

        >>> ca = ClientAdapter( api_id, api_hash )
        >>> ca.plot_message_times('+11234567891',limit=1)
        >>> ca.plot_message_times('quartz_husky',limit=1)
        """

        times=get_all_message_date_times(username,limit)

        df = pd.DataFrame({'hour':times})
        plot = df.groupby(df['hour'].dt.hour).count().plot(kind='bar')

        return plot
