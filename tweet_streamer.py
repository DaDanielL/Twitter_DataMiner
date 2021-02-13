import os
import webbrowser
import json

import tweepy
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener


class TweetStream(StreamListener):

    def on_data(self, data):
        try:
            with open('data/tweets.json', 'a') as file:
                file.write(data)
            Twitter.count_tweet()

        except BaseException as error:
            print("Error on_data: %s" % str(error))
        
        finally:
            return True

    def on_error(self, status):
        return False


class StreamHandler():

    def __init__(self):
        self.numTweet = 0

    def get_auth(self):
        consumer_key = 'ZhzMMSN3QExyjrkFYrZU1GqNY'
        consumer_secret = 'fihs6teRdhCP8PaB2Rrn0VoZZpxl4oyU6Kh0weg8jTqW5wxZlA'

        callback_url = 'oob'

        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)

        self.redirect_url = self.auth.get_authorization_url()
        webbrowser.open(self.redirect_url)


    def set_auth(self,pin):
        self.auth.get_access_token(pin)
        api = tweepy.API(self.auth)


    def start_stream(self, b, search=['the','a','is','are','I','you','what','how','he','she','they','it']):

        with open('data/tweets.json','w') as f:
            json_str = json.dumps(search)
            f.seek(1)
            f.write(json_str)

        if b == True:
            self.TweetStreamer = Stream(self.auth, TweetStream())
            self.TweetStreamer.filter(track = search,languages=["en"],is_async=True)

        elif b == False:
            self.TweetStreamer.disconnect()


    def count_tweet(self):
        try: 
            self.numTweet += 1
        except:
            self.numTweet = 0
   
Twitter = StreamHandler()