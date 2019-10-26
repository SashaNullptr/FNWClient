from prometheus_client import Gauge, Histogram

sentiment_gauge = Gauge('sentiment', 'Average sentiment')
contact_times = Histogram('message_times', 'Message send time')
