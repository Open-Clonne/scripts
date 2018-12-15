import tweepy
import time
from keys import *

print('booting up Grayson twitterbot', flush=True)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'id.txt'

def retrieve_id(file_name):
    f_read = open(file_name, 'r')
    id = int(f_read.read().strip())
    f_read.close()
    return id

def store_id(id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(id))
    f_write.close()
    return

def clonnebot():
    print('retrieving and replying to Grayson twitterbot tweets...', flush=True)

    id = retrieve_id(FILE_NAME)
    mentions = api.mentions_timeline(id, tweet_mode='extended')

    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        id = mention.id
        store_id(id, FILE_NAME)

        if '#grayTheExpert' in mention.full_text.lower():
            print('Grayson twitterbot found #grayTheExpert!', flush=True)
            print('Grayson twitterbot responding back...', flush=True)
            api.update_status('@' + mention.user.screen_name + '#grayTheExpert back to you!', mention.id)

while True:
    clonnebot()
    time.sleep(15)