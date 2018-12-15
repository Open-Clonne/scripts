import time
import tweepy
from keys import *
from hackernews import HackerNews

print('booting up Grayson twitterbot', flush=True)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

CLONNEBOTS = '@natgraybillz @GurdipPradip @jptwerpsall @clonne101'


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

    mentions = api.mentions_timeline(lid, tweet_mode='extended')

    for mention in reversed(mentions):
        try:
            lid = mention.id
            store_id(lid, 'user_status.txt')

            if '#graytheexpert' in mention.full_text.lower():
                print('found hash-tag and responding, liking and re-tweeting now', flush=True)
                api.update_status(
                    '@' + mention.user.screen_name + ' good read there, thanks sir #grayTheExpert', mention.id
                )
                api.retweet(mention.id)
                mention.favorite()

        except tweepy.TweepError as e:
            print('Error Message: ' + get_exception_message(e.reason))

        except StopIteration:
            break


def update_home_timeline():
    print('\n')
    print('home timeline management...', flush=True)

    lid = retrieve_id('timeline.txt')
    if not lid:
        print('no lid found')

    timeline = api.home_timeline(lid)

    for timeline_tweet in reversed(timeline):
        try:
            print('liking and re-tweeting ' + timeline_tweet.id + ' tweets in timeline now...', flush=True)

            lid = timeline_tweet.id
            store_id(lid, 'timeline.txt')

            timeline_tweet.favorite()
            timeline_tweet.retweet()

        except tweepy.TweepError as e:
            print('Error Message: ' + get_exception_message(e.reason))

        except StopIteration:
            break


def update_follow_followers():
    print('\n')
    print('following followers...', flush=True)

    user = api.me()
    followers = api.followers(user.id)

    for follower in reversed(followers):
        try:
            if not follower.following:
                if follower.id == user.id:
                    print('Not following self, passing on...')
                    continue
                else:
                    follower.follow()
                    print("Followed everyone that is following " + user.name)
            else:
                print('All following has been completed and none found so finding user followers')
                find_user_followers(follower.id)

        except tweepy.TweepError as e:
            print('Error Message: ' + get_exception_message(e.reason))

        except StopIteration:
            break


def find_user_followers(user_id):
    print('\n')
    print('Finding user and followers and following them')

    user = api.get_user(user_id)
    followers = api.followers(user_id)

    for follower in reversed(followers):
        try:
            if follower.following:
                print('Already following ' + follower.name + ' so moving on...')
                continue
            else:
                if follower.id == user.id:
                    print('Not following self, passing on...')
                    continue
                else:
                    follower.follow()
                    print("Followed everyone that is following " + user.name)

        except tweepy.TweepError as e:
            print('Error Message: ' + get_exception_message(e.reason))

        except StopIteration:
            break


def update_user_status_hacker_news():
    print('\n')
    print('getting latest news from hacker_news and updating user status...', flush=True)

    hn = HackerNews()

    stories = hn.top_stories(limit=15)

    for story in stories:
        try:

            lid_r = retrieve_id('hacker_news.txt')

            lid = story.item_id

            if lid > lid_r:
                print('saving new lid now')
                store_id(lid, 'hacker_news.txt')
                print('hacker_news top story, responding, liking and re-tweeting now', flush=True)
                tweet = api.update_status(story.title + '\n' + story.url + '\n By: ' + story.by + '\n' + CLONNEBOTS)
                tweet.retweet()
                tweet.favorite()
            else:
                print('no new top stories are available at this time', flush=True)

        except tweepy.TweepError as e:
            print('Error Message: ' + get_exception_message(e.reason))

        except StopIteration:
            break


while True:
    #update_user_mentions()
    #update_home_timeline()
    #update_follow_followers()
    update_user_status_hacker_news()
    time.sleep(100)
