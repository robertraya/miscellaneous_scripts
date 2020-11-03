import tweepy
import json
import re
import os
from os import path
import shutil
from nltk.tokenize import word_tokenize
from tweepy import OAuthHandler
 
consumer_key = 'YOUR-CONSUMER-KEY'
consumer_secret = 'YOUR-CONSUMER-SECRET'
access_token = 'YOUR-ACCESS-TOKEN'
access_secret = 'YOUR-ACCESS-SECRET'

#consumer_key and then consumer_secret 
auth = tweepy.OAuthHandler('LTGtSJVaCJMMiDl3XMEG9L6WA', '5VODl4xjEU0Z5IzCeBfJ8Q6OT99vTCP4msOkYVQNb6VXWKN9sA')
#access_token and access_secret
auth.set_access_token('24237196-BpcC48I5yramFLsgT4Ul1wo5q2b3hqLON9isQEUue', 'lYqnnI5oYDknAm1mAeACxxKGOQLqJWWBMzm1rmYiyafn4')
 
api = tweepy.API(auth)

#regex shit
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

#defining function to print out tweets 
def process_or_store(tweet):
    with open('mytweets.json', 'w') as file:
        json.dump(tweet, file)

#for loop to iterate through my own timeline
# for status in tweepy.Cursor(api.home_timeline).items(10):
#     # Process a single status
#     process_or_store(status._json)

#all of my tweets
for tweet in tweepy.Cursor(api.user_timeline).items():
    process_or_store(tweet._json)

    
 
# #opening and cleaning
with open('mytweets.json', 'r') as f:
    for line in f:
        tweet = json.loads(line)
        tokens = preprocess(tweet['text'])
        # process_or_store(tokens)
#         # shutil.move('/Users/robertraya/PythonProjects/Dev/mytweets.json', os.getcwd())