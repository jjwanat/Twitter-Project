# encoding: utf-8
import tweepy

# Set User Credential variables to access Twitter API
access_token = "50069664-tV7WMv1yUvG9eKii1fp1RpAIMfaiGqnUbI7ZrD69v"
access_token_secret = "xQAD0CSmSlCmuYDyA4dD5RzHMENM7mT8UxPjNyp7kcLWd"
consumer_key = "EA4ROi614f8nXePnFwhbJ25tv"
consumer_secret = "jSGxdUnLLK3yxdgjiMz4PaI56INpmWEmC1Fi1JiBbYESa4UrUO"

class MyStream(tweepy.StreamListener):
    def __init__(self):
        tweepy.StreamListener.__init__(self)

    def on_status(self, tweet):
        hashtags = [hashtag["text"] for hashtag in tweet.entities["hashtags"]]
        print hashtags


def main():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    emotions = ["#love", "#blessed", "#hate", "#smile", "#happy", "#thanks", "#ferguson", "#sad", "#good", "#bad"]

    stream = tweepy.Stream(auth, MyStream(), timeout=50)
    stream.filter(track=emotions)


if __name__ == "__main__":
    main()

