import json

class TimeSentimentVariance:

    def __init__(self,time,sentiment,variance):
        self.__time = time
        self.__sentiment = sentiment
        self.__variance = variance

    def time(self):
        return self.__time

    def sentiment(self):
        return self.__sentiment

    def variance(self):
        return self.__variance

class STVEncoder(JSONEncoder):
        def default(self, o):
            return {"time":o.time(),"sentiment":o.sentiment(),"Variance":o.variance()}
