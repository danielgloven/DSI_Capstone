import tweepy
import sys
import json
from collections import defaultdict

class MyStreamListener(tweepy.StreamListener):
    "Listener for streaming data"

    def __init__(self):
        self.outfile = "../data_dumps/test.json" # Put streaming tweets in this file

    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        try:
            with open(self.outfile, 'a') as f:
                f.write(data)
                print(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        print(status)
        return True

if __name__ == '__main__':
    # Get OAuth Authentication from keys.txt file which is included in .gitignore
    keys = defaultdict()
    with open('twitter_keys.txt') as f:
        for line in f:
            keys[line.split()[0]] = line.split()[-1]

    auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])

    api = tweepy.API(auth)

    # Get Tweets on my home page
    # public_tweets = api.home_timeline()
    # for tweet in public_tweets:
    #     print tweet._json

    # Stream Tweets with filter
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    myStream.filter(track=['boulder'])

    # Cursor example
    # for tweet in tweepy.Cursor(api.user_timeline).items():
    #     print tweet._json
