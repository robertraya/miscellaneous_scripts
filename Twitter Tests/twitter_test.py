#tracking live twitter data application

#importing twitter module

#!/usr/bin/env/python3

import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

auth = tweepy.OAuthHandler('LTGtSJVaCJMMiDl3XMEG9L6WA', '5VODl4xjEU0Z5IzCeBfJ8Q6OT99vTCP4msOkYVQNb6VXWKN9sA')
auth.set_access_token('24237196-BpcC48I5yramFLsgT4Ul1wo5q2b3hqLON9isQEUue', 'lYqnnI5oYDknAm1mAeACxxKGOQLqJWWBMzm1rmYiyafn4')

api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)

user_input = input('Enter topic you want to see: ')

myStream.filter(track=[user_input])


