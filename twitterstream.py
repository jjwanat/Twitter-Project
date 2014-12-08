# encoding: utf-8
import sys
import os

# Import third party libraries
import json
import pandas as pd
import tweepy

# Set User Credential variables to access Twitter API
access_token = "50069664-tV7WMv1yUvG9eKii1fp1RpAIMfaiGqnUbI7ZrD69v"
access_token_secret = "xQAD0CSmSlCmuYDyA4dD5RzHMENM7mT8UxPjNyp7kcLWd"
consumer_key = "EA4ROi614f8nXePnFwhbJ25tv"
consumer_secret = "jSGxdUnLLK3yxdgjiMz4PaI56INpmWEmC1Fi1JiBbYESa4UrUO"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print tweet.entities['hashtags'["text"]]
