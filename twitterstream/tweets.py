# encoding: utf-8
from collections import Counter
from prettytable import PrettyTable
import twitter
import json

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
    try:
        next_results = results['search_metadata']['next_results']
    except KeyError, e:  # No more results when next_results doesn't exist
        break

    kwargs = dict([kv.split('=') for kv in next_results[1:].split("&")])

    results = twitter_api.search.tweets(**kwargs)
    statuses += results['statuses']

# Get the text from the tweets
status_texts = [status['text'] for status in statuses]

# Get User Screen Names from tweets
screen_names = [user_mention['screen_name']
                for status in statuses
                for user_mention in status['entities']['user_mentions']]

# Get the Hashtags used
hashtags = [hashtag['text']
            for status in statuses
            for hashtag in status['entities']['hashtags']]

# Compute a collection of all words from all tweets
words = [w for t in status_texts for w in t.split()]

# Print out a prettytable using the most common words, names, and hashtags
for label, data in (('Word', words),
                    ('Screen Name', screen_names),
                    ('Hashtag', hashtags)):
    pt = PrettyTable(field_names=[label, 'Count'])
    c = Counter(data)
    [pt.add_row(kv) for kv in c.most_common()[:10]]
    pt.align[label], pt.align['Count'] = 'l', 'r'
    print pt

retweets = [(status['retweet_count'],
             status['retweeted_status']['user']['screen_name'],
             status['text'])

            for status in statuses
            if status.has_key('retweeted_status')
]

# Slice off the first 5 from the sorted results and display each item in the tuple
pt = PrettyTable(field_names=['Count', 'Screen Name', 'Text'])
[pt.add_row(row) for row in sorted(retweets, reverse=True)[:5]]
pt.max_width['Text'] = 50
pt.align = 'l'
print pt