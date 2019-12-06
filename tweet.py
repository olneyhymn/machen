import os
import twitter as tw
import logging
import time

from nodb import NoDB
from random import shuffle

tweet_content = "tweet-content.txt"
tweet_lookup = "tweet-lookup.shelve"
logging.basicConfig(filename="tweet.log", level=logging.WARNING)


def get_raw_tweets():
    tweets = []
    with open(tweet_content, "r", encoding="utf-8") as f:
        raw_tweets = f.readlines()
        for tweet in raw_tweets:
            tweets.append(tweet.strip())
    return tweets


def send_tweet(s, db):
    cred = {
        "consumer_key": os.environ["CONSUMER_KEY"].strip(),
        "consumer_secret": os.environ["CONSUMER_SECRET"].strip(),
        "token": os.environ["TOKEN"].strip(),
        "token_secret": os.environ["TOKEN_SECRET"].strip(),
    }
    auth = tw.OAuth(**cred)
    t = tw.Twitter(auth=auth)
    t.statuses.update(status=s)
    print("Sent tweet: {}".format(s))

    db.save({"content": s, "last_sent": int(time.time()), "from": "machen"})


def get_db(bucket="olneyhymnbots", serializer="json", index="content"):
    db = NoDB()
    db.bucket = bucket
    db.human_readable_indexes = True
    db.serializer = serializer
    db.index = index
    return db


def tweets_ordered_by_last_sent_time(db):
    last_sent = {}
    for tweet in get_raw_tweets():
        d = db.load(tweet)
        if d is None:
            last_sent[tweet] = 0
        else:
            last_sent[tweet] = d["last_sent"]
    s = sorted([(time, tweet) for tweet, time in last_sent.items()])
    return [t for _, t in s]


def tweet(a, b):
    db = get_db()
    tweets = tweets_ordered_by_last_sent_time(db)
    tweets = tweets[0:10]
    shuffle(tweets)
    tweet = tweets[0]
    tweet = tweet.replace(" / ", "\n")
    send_tweet(tweet, db)


if __name__ == "__main__":
    tweet()
