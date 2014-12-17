import tweepy
import sys
import pika
import json
import time

#get your own twitter credentials at dev.twitter.com
access_token = "50069664-tV7WMv1yUvG9eKii1fp1RpAIMfaiGqnUbI7ZrD69v"
access_token_secret = "xQAD0CSmSlCmuYDyA4dD5RzHMENM7mT8UxPjNyp7kcLWd"
consumer_key = "EA4ROi614f8nXePnFwhbJ25tv"
consumer_secret = "jSGxdUnLLK3yxdgjiMz4PaI56INpmWEmC1Fi1JiBbYESa4UrUO"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener, self).__init__()

        #setup rabbitMQ Connection
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = connection.channel()

        #set max queue size
        args = {"x-max-length": 2000}

        self.channel.queue_declare(queue='twitter_topic_feed', arguments=args)

    def on_status(self, status):
        print status.text, "\n"

        data = {}
        data['text'] = status.text
        data['created_at'] = time.mktime(status.created_at.timetuple())
        data['geo'] = status.geo
        data['source'] = status.source

        #queue the tweet
        self.channel.basic_publish(exchange='',
                                    routing_key='twitter_topic_feed',
                                    body=json.dumps(data))

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True  # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True  # Don't kill the stream

sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))
# my keyword today is chelsea as the team just had a big win
sapi.filter(track=['happy', 'sad'])  