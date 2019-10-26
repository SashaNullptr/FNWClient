import asyncio
from datetime import datetime
from dateutil import tz
from itertools import groupby
import re
from statistics import mean, stdev

from telethon.sync import TelegramClient
import pandas as pd
from textblob import TextBlob

from services.time_sentiment_vairance import TimeSentimentVariance

class TelegramAnalytics:
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

        >>> ca = TelegramAnalytics( api_id, api_hash )
        >>> ca.get_all_message_date_times('+11234567891',limit=1)
        >>> ca.get_all_message_date_times('quartz_husky',limit=1)
        """
        return list(map( lambda x: x.date.astimezone(self.__to_zone), self.__client.iter_messages(username,limit=limit)))

    def get_all_message_times(self, username,limit=10):
        """
        Get time stamps (hours, minutes, seconds, microseconds)
        for all messages exchanged between you and an entity.

        :param str username: Username (or phone number) of entity to get chat history from.
        :param int limit: The number of messages to extract information from.

        :return: Array of times that each messages was sent.
        :rtype: [datetime.time]

        >>> ca = TelegramAnalytics( api_id, api_hash )
        >>> ca.get_all_message_date_times('+11234567891',limit=1)
        >>> ca.get_all_message_date_times('quartz_husky',limit=1)
        """
        return list(map( lambda x: x.date.astimezone(self.__to_zone).time(), self.__client.iter_messages(username,limit=limit)))

    def message_time_histogram(self,username,limit=10):
        """
        Get a time histrogram for all messages exchanged between you and an entity.

        :param str username: Username (or phone number) of entity to get chat history from.
        :param int limit: The number of messages to extract information from.

        >>> from fnw_client import TelegramAnalytics
        >>> import matplotlib.pyplot as plt
        >>>
        >>> plt.figure()
        >>>
        >>> ca = TelegramAnalytics( api_id, api_hash )
        >>> time_historgram = ca.message_time_histogram('quartz_husky',limit=100)
        >>> time_histogram.plot(kind='bar')
        >>>
        >>> plt.show()
        """

        times = get_all_message_date_times(username,limit)
        df = pd.DataFrame({'hour':times})
        return df.groupby(df['hour'].dt.hour).count()

    def __text_sentiment(self,text):

        def clean_text(self,text):
            return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())

        cln_text = clean_text(text)
        return None if not cln_text else TextBlob(cln_text).sentiment.polarity

    def get_sentiments(self,username,limit=10):

        message_iterator = self.__client.iter_messages(username,limit=limit)
        return [ self.__text_sentiment(x.text) for x in message_iterator if isinstance(x.text,str)]

    def message_sentiment_histogram(self,username,limit=10):
        """
        Get a sentiment histrogram for all messages exchanged between you and an entity.
        """

        sentiments = get_sentiments(username,limit)
        df=pd.DataFrame({'sentiment':sentiments})
        # Remove zero values and NAs
        df_nz = df[(df.T != 0).any()].dropna()
        return df_nz.hist(bins=20)

    def message_sentiment_rolling_avg(self,username,limit=10):
        """
        Get rolling average data of all messages exchanged between you and an entity.
        """

        sentiments = get_sentiments(username,limit)
        df=pd.DataFrame({'sentiment':sentiments})
        # Remove zero values and NAs
        df_nz = df[(df.T != 0)].any().dropna()
        rolling_avg_factor = int(df_nz.shape[0]/100)+1
        return df_nz.rolling(rolling_avg_factor).mean()

    def message_sentiment_vs_time(self,username,limit=10):
        """
        Get a graph of sentiment as a function of hour of the day.

        :param str username: Username (or phone number) of entity to get chat history from.
        :param int limit: The number of messages to extract information from.

        :return: A tuple with the following format: (hour,sentiment,variance-in-sentiment)
        :rtype: (int,float,float)

        >>> from fnw_client import TelegramAnalytics
        >>> import matplotlib.pyplot as plt
        >>>
        >>> plt.figure()
        >>>
        >>> ca = TelegramAnalytics( api_id, api_hash )
        >>> sentiment_and_time = ca.message_sentiment_and_time('quartz_husky',limit=100)
        >>> variances = [ x.variance() for x in sentiment_and_time ]
        >>>
        >>> plt.bar(range(len(sentiment_and_time)), [val.sentiment() for val in sentiment_and_time], align='center',yerr=variances)
        >>> plt.xticks(range(len(sentiment_and_time)), [val.time() for val in sentiment_and_time])
        >>> plt.xticks(rotation=70)
        >>> plt.xlabel('Hour')
        >>> plt.ylabel('Average Sentiment')
        >>>
        >>> plt.show()
        """

        class TimeAndSentiment:

            def __init__(self,time,sentiment):
                self.__time = time
                self.__sentiment = sentiment

            def time(self):
                return self.__time

            def sentiment(self):
                return self.__sentiment

        def get_sentiments_and_times(self,username,limit=10):

            message_iterator = self.__client.iter_messages(username,limit=limit)

            get_datetime = lambda x: x.date.astimezone(self.__to_zone).time()
            get_sentiment = lambda x: self.__text_sentiment(x.text)

            ts = [ TimeAndSentiment(get_datetime(x),get_sentiment(x)) for x in message_iterator if isinstance(x.text,str)]
            # Sorted output by hours, which is necessary for groupby to work properly
            return sorted(ts,key=lambda x: x.time().hour)

        hour_group = groupby(get_sentiments_and_times(username,limit), lambda x: x.time().hour)
        average_sentiment = lambda group : mean([ x.sentiment() for x in group if x.sentiment() is not None])

        def stdev_sentiment(group):
            clean_group = [x for x in group if x.sentiment() is not None]
            return stdev([ x.sentiment() for x in clean_group]) if (len(clean_group) >= 2) else 0

        return [TimeSentimentVariance(key,average_sentiment(group),stdev_sentiment(group)) for key, group in hour_group]
