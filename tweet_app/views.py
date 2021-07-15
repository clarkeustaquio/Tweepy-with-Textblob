import os
import tweepy
from textblob import TextBlob
from django.shortcuts import render


def index(request):
    consumer_key = os.environ.get('consumer_key')
    consumer_secret = os.environ.get('consumer_secret')

    access_token = os.environ.get('access_token')
    access_token_secret = os.environ.get('access_token_secret')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    search = str()
    context = dict()
    results = list()
    filter = '-filter:retweets'

    positive_percentage = 0
    negative_percentage = 0
    neutral_percentage = 0

    if request.method == 'POST':
        search += request.POST['tweet_search'].strip()

        query = "{} {}".format(search, filter)
        searches = api.search(q=query, count=100)
        
        positive = 0
        negative = 0
        neutral = 0

        for result in searches:
            tweet = result.text.strip()
            results.append(tweet)
            blob = TextBlob(tweet)

            polarity = blob.sentiment.polarity
            if polarity == 0:
                neutral += 1
            elif polarity < 0:
                negative += 1
            elif polarity > 0:
                positive += 1

        total = positive + negative + neutral
        positive_percentage = float((positive * 100) / total)
        negative_percentage = float((negative * 100) / total)
        neutral_percentage = float((neutral * 100) / total)

    context = {
        'results': results,
        'positive': positive_percentage,
        'negative': negative_percentage,
        'neutral': neutral_percentage
    }

    return render(request, 'tweet_app/index.html', context=context)