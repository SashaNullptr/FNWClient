from telethon.sync import TelegramClient
import pandas as pd
import asyncio

from datetime import datetime
from dateutil import tz

class ClientAdapter:
    """
    A client that connects to Telegram.
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

    def get_all_message_times(self, username,limit=10):
        return list(map( lambda x: x.date.astimezone(to_zone).time(), self.__client.iter_messages(username,limit=limit)))

    def get_all_message_date_times(self, username,limit=10):
        return list(map( lambda x: x.date.astimezone(to_zone), self.__client.iter_messages(username,limit=limit)))

    def plot_message_times(self,username,limit=10):

        times=get_all_message_times(username,limit)

        df = pd.DataFrame({'date':times})
        df.set_index('date', drop=False, inplace=True)
        df.groupby(pd.TimeGrouper(freq='10Min')).count().plot(kind='bar')

        return df.hist(bins=24)
