# encoding: utf-8
import tweepy

# Set User Credential variables to access Twitter API
access_token = "50069664-tV7WMv1yUvG9eKii1fp1RpAIMfaiGqnUbI7ZrD69v"
access_token_secret = "xQAD0CSmSlCmuYDyA4dD5RzHMENM7mT8UxPjNyp7kcLWd"
consumer_key = "EA4ROi614f8nXePnFwhbJ25tv"
consumer_secret = "jSGxdUnLLK3yxdgjiMz4PaI56INpmWEmC1Fi1JiBbYESa4UrUO"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

emotions = ["#love", "#blessed", "#hate", "#smile", "#happy", "#thanks", "#ferguson", "#sad", "#good", "#bad"]

for emotion in emotions:
    for tweet in tweepy.Cursor(api.search, q=emotion, since="2014-11-27", until="2014-12-01").items():
        print tweet.text

#stream = tweepy.Stream(auth, timeout=50)
#stream.filter(track=emotions)

