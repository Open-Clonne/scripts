import time
import tweepy
from keys import *

print('booting up reporterBot[Grayson]', flush=True)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


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


def get_exception_message(msg):
    words = msg.split(' ')

    error_message = ""
    for index, word in enumerate(words):
        if index not in [0, 1, 2]:
            error_message = error_message + ' ' + word

    error_message = error_message.rstrip("\'}]")
    error_message = error_message.lstrip(" \'")

    return error_message


def update_user_mentions():
    print('\n')
    print('retrieving and replying to hash-tags...', flush=True)

    lid = retrieve_id('user_status.txt')
    if not lid:
        print('no lid found')

    print('checking remaining request count...')
    remaining = None
    try:
        remaining = api.rate_limit_status()['resources']['application']['/application/rate_limit_status']['remaining']
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    mentions = None
    try:
        mentions = api.mentions_timeline(lid, tweet_mode='extended')
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    for mention in reversed(mentions):
        try:

            if remaining > 30:

                if '#graytheexpert' in mention.full_text.lower():
                    print('found hash-tag and responding, liking and re-tweeting now', flush=True)
                    api.update_status(
                        '@' + mention.user.screen_name + ' good read there, thanks sir, happy tweeting ' + HASH_TAGS, mention.id
                    )
                    api.retweet(mention.id)
                    mention.favorite()
                else:
                    print('no hash-tag found so responding, liking and re-tweeting now', flush=True)
                    api.update_status(
                        '@' + mention.user.screen_name + ' good read there, thanks! ' + HASH_TAGS, mention.id
                    )
                    api.retweet(mention.id)
                    mention.favorite()

                lid = mention.id
                store_id(lid, 'user_status.txt')

            else:
                print('User mention respond, liking and re-tweeting exceeded for now...')

        except tweepy.TweepError as e:
            print('Error Message: ' + get_exception_message(e.reason))

        except StopIteration:
            break


while True:

    # timeout
    timeout = 10000.0

    # mentions
    try:
        update_user_mentions()
    except Exception as e:
        print('Error Message: ' + str(e))

    # boot
    time.sleep(timeout)
