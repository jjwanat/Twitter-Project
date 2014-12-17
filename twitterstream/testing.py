# encoding: utf-8
from collections import Counter
from prettytable import PrettyTable
import pandas as pd
import twitter
import matplotlib.pyplot as plt

# Set User Credential variables to access Twitter API
access_token = "50069664-tV7WMv1yUvG9eKii1fp1RpAIMfaiGqnUbI7ZrD69v"
access_token_secret = "xQAD0CSmSlCmuYDyA4dD5RzHMENM7mT8UxPjNyp7kcLWd"
consumer_key = "EA4ROi614f8nXePnFwhbJ25tv"
consumer_secret = "jSGxdUnLLK3yxdgjiMz4PaI56INpmWEmC1Fi1JiBbYESa4UrUO"

# Set Twitter Auth
auth = twitter.oauth.OAuth(access_token, access_token_secret, consumer_key, consumer_secret)
twitter_api = twitter.Twitter(auth=auth)

# Set emotions to search
emotions = ['#happy', '#sad', '#love', '#hate', '#blessed']
statuses = []

# Search and Store
for emotion in emotions:
    results = twitter_api.search.tweets(q=emotion, count=100)
    statuses += results['statuses']

for _ in range(5):
    print "Length of statuses", len(statuses)
    try:
        next_results = results['search_metadata']['next_results']
    except KeyError, e: # No more results when next_results doesn't exist
        break

    kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])

    results = twitter_api.search.tweets(**kwargs)
    statuses += results['statuses']

# Get the text from the tweets
status_texts = [ status['text'] for status in statuses ]

# Get User Screen Names from tweets
screen_names = [ user_mention['screen_name']
        for status in statuses
        for user_mention in status['entities']['user_mentions'] ]

# Get the Hashtags used
hashtags = [ hashtag['text']
        for status in statuses
        for hashtag in status['entities']['hashtags'] ]

# Compute a collection of all words from all tweets
words = [ w for t in status_texts for w in t.split() ]

df = pd.DataFrame(data=statuses)
print df.columns
# df.plot(kind='bar')
# plt.plot(hashtags)
