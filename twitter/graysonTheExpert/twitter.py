import tweepy
import time
from keys import *

print('booting up Grayson twitterbot', flush=True)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'lid.txt'

def retrieve_id(file_name):
    f_read = open(file_name, 'r')
    lid = int(f_read.read().strip())
    f_read.close()
    return lid

def store_id(lid, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(lid))
    f_write.close()
    return

def getExceptionMessage(msg):
    words = msg.split(' ')

    errormsg = ""
    for index, word in enumerate(words):
        if index not in [0, 1, 2]:
            errormsg = errormsg + ' ' + word

    errormsg = errormsg.rstrip("\'}]")
    errormsg = errormsg.lstrip(" \'")

    return errormsg

def update_status_bot():
    print('retrieving and replying to Grayson twitterbot hashtags...', flush=True)

    lid = retrieve_id(FILE_NAME)
    if not lid:
        print('no lid found')

    mentions = api.mentions_timeline(lid, tweet_mode='extended')

    for mention in reversed(mentions):
        try:
            lid = mention.id
            store_id(lid, FILE_NAME)

            if '#graytheexpert' in mention.full_text.lower():
                print('Grayson twitterbot found hashtag and responding', flush=True)
                api.update_status('@' + mention.user.screen_name + '#grayTheExpert back to you!', mention.id)
                print('Grayson twitterbot re-tweeting now', flush=True)
                api.retweet(mention.id)

        except tweepy.TweepError as e:
            print('Error Code: ' + e.api_code)
            print('Error Message: ' + getExceptionMessage(e.reason))

def update_home_timeline():
    print('home timeline management...', flush=True)

    lid = retrieve_id(FILE_NAME)
    if not lid:
        print('no lid found')

    timeline = api.home_timeline(lid)
    print('timeline data : ' + timeline)
    exit()

while True:
    update_home_timeline()
    time.sleep(15)