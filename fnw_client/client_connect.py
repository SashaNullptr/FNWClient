from telethon.sync import TelegramClient, events
import pandas as pd
import asyncio

class ClientAdapter:
    """
    A client that connects to Telegram.
    """

    def __init__(self, api_id, api_hash):

        self.__api_id = api_id
        self.__api_hash = api_hash

        self.__client = TelegramClient('session_name', api_id, api_hash)
        self.__client.start()

    def __del__(self):
        self.__client.disconnect()

    def get_all_message_times(self, username,limit=10):
        return list(map( lambda x: x.date.time(), self.__client.iter_messages(username,limit=limit)))

        # times = []
        # for message in self.__client.iter_messages(username):
        #     times.append(message.date.time())
        # return await li

    def plot_message_times(self,username,limit=10):

        times=get_all_message_times(username,limit)

        df = pd.DataFrame({'date':times})
        df.set_index('date', drop=False, inplace=True)
        df.groupby(pd.TimeGrouper(freq='10Min')).count().plot(kind='bar')

        return df.hist(bins=12)
