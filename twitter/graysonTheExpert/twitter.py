import tweepy
import time
from keys import *

print('booting up Grayson twitterbot', flush=True)

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

    errormsg = ""
    for index, word in enumerate(words):
        if index not in [0, 1, 2]:
            errormsg = errormsg + ' ' + word

    errormsg = errormsg.rstrip("\'}]")
    errormsg = errormsg.lstrip(" \'")

    return errormsg


def update_user_status():
    print('retrieving and replying to hashtags...', flush=True)

    lid = retrieve_id('user_status.txt')
    if not lid:
        print('no lid found')

    mentions = api.mentions_timeline(lid, tweet_mode='extended')

    for mention in reversed(mentions):
        try:
            lid = mention.id
            store_id(lid, 'user_status.txt')

            if '#graytheexpert' in mention.full_text.lower():
                print('found hashtag and responding and retweeting now', flush=True)
                api.update_status('@' + mention.user.screen_name + '#grayTheExpert back to you!', mention.id)
                api.retweet(mention.id)

        except tweepy.TweepError as e:
            print('Error Code: ' + e.api_code)
            print('Error Message: ' + get_exception_message(e.reason))


def update_home_timeline():
    print('home timeline management...', flush=True)

    lid = retrieve_id('timeline.txt')
    if not lid:
        print('no lid found')

    timeline = api.home_timeline(lid)

    for timeline_tweet in reversed(timeline):
        try:
            print('liking and retweeting all tweets in timeline now...', flush=True)

            lid = timeline_tweet.id
            store_id(lid, 'timeline.txt')

            timeline_tweet.favorite()
            timeline_tweet.retweet()

        except tweepy.TweepError as e:
            print('Error Message: ' + get_exception_message(e.reason))

        except StopIteration:
            break


def update_follow_followers():
    print('following followers...', flush=True)

    user = api.me()
    print(user)
    exit()

    for follower in tweepy.Cursor(api.followers).items():
        follower.follow()
        print("Followed everyone that is following " + user.name)


while True:
    update_follow_followers()
    time.sleep(100)
