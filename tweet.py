import schedule
import time
import os
import shelve
import twitter as tw
import boto.dynamodb
import logging

from random import shuffle

tweet_content = "tweet-content.txt"
tweet_lookup = "tweet-lookup.shelve"
logging.basicConfig(filename='tweet.log', level=logging.WARNING)


def initialize():
    tweets = shelve.open(tweet_lookup)
    with open(tweet_content, 'r') as f:
        raw_tweets = f.readlines()
        for tweet in raw_tweets:
            tweets[tweet.strip()] = 0
    tweets.close()


def send_tweet(s):
    cred = {
        "consumer_key": os.environ['MACHEN_CONSUMER_KEY'],
        "consumer_secret": os.environ['MACHEN_CONSUMER_SECRET'],
        "token": os.environ['MACHEN_TOKEN'],
        "token_secret": os.environ['MACHEN_TOKEN_SECRET'],
    }
    auth = tw.OAuth(**cred)
    t = tw.Twitter(auth=auth)
    t.statuses.update(status=s)
    print("Sent tweet: {}".format(s))


def tweet():
    lookup = shelve.open(tweet_lookup)
    tweets = list(lookup.keys())
    tweets = sorted(tweets, key=lambda tweet: lookup[tweet])
    tweets = tweets[0:10]
    shuffle(tweets)
    tweet = tweets[0]
    lookup[tweet] += 1
    send_tweet(tweet)
    lookup.close()


if __name__ == '__main__':
    if not os.path.isfile(tweet_lookup + ".db"):
        initialize()

    tweet()
    schedule.every(1256).minutes.do(tweet)

    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            logging.error(e)
        time.sleep(60)
