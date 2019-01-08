import time
import tweepy
import requests
from keys import *

print('booting up clonneBot[Jones]', flush=True)

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


def update_home_timeline():
    print('\n')
    print('home timeline management...', flush=True)

    lid = retrieve_id('timeline.txt')
    if not lid:
        print('no lid found')

    print('checking remaining request count...')
    remaining = None
    try:
        remaining = api.rate_limit_status()['resources']['application']['/application/rate_limit_status']['remaining']
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    timeline = None
    try:
        timeline = api.home_timeline(lid)
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    for timeline_tweet in reversed(timeline):
        try:

            if remaining > 50:
                print('liking and re-tweeting ' + str(timeline_tweet.id) + ' tweets in timeline now...', flush=True)

                timeline_tweet.favorite()
                timeline_tweet.retweet()

                lid = timeline_tweet.id
                store_id(lid, 'timeline.txt')
            else:
                print('Timeline likes and re-tweets exceeded for now...')

        except tweepy.TweepError as e:
            print('Error Message: ' + get_exception_message(e.reason))

        except StopIteration:
            break


def update_follow_followers():
    print('\n')
    print('following all new followers...', flush=True)

    print('checking remaining request count...')
    remaining = ''
    try:
        remaining = api.rate_limit_status()['resources']['application']['/application/rate_limit_status']['remaining']
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    followers = None
    user = None
    try:
        user = api.me()
        followers = api.followers(user.id)
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    if (user.friends_count < 1000) and (user.followers_count + 500) < 1000:
        for follower in reversed(followers):
            try:
                if not follower.following:
                    if follower.id == user.id:
                        print('Not following self, passing on...')
                        continue
                    else:
                        if remaining > 160:
                            follower.follow()
                            print("Followed everyone that is following " + user.name)
                        else:
                            print('Follow limit exceeded, no more following for now')
                            break
                else:
                    if remaining > 160:
                        print('All following has been completed and none found so finding user followers')

                        print('\n')
                        print('Finding user and followers and following them')

                        f_user = None
                        try:
                            f_user = api.get_user(follower.id)
                        except tweepy.TweepError as e:
                            print('Error Message: ' + get_exception_message(e.reason))

                        f_followers = api.followers(follower.id)

                        if (user.friends_count < 1000) and (user.followers_count + 500) < 1000:

                            for f_follower in reversed(f_followers):
                                try:
                                    if (user.friends_count < 1000) and (user.followers_count + 500) < 1000:
                                        print('Following has been put on hold till followers pick up')
                                        break

                                    if f_follower.following:
                                        print('Already following ' + f_follower.name + ' so moving on...')
                                        continue
                                    else:
                                        if f_follower.id == f_user.id:
                                            print('Not following self, passing on...')
                                            continue
                                        else:
                                            if remaining > 160:
                                                f_follower.follow()
                                                print("Followed everyone that is following " + f_user.name)
                                            else:
                                                print('Follow limit exceeded, no more following for now')
                                                break

                                except tweepy.TweepError as e:
                                    print('Error Message: ' + get_exception_message(e.reason))

                                except StopIteration:
                                    break
                        else:
                            print('Following has been put on hold till followers pick up')

                    else:
                        print('Follow limit exceeded, no more following for now')
                        break

            except tweepy.TweepError as e:
                print('Error Message: ' + get_exception_message(e.reason))

            except StopIteration:
                break
    else:
        print('Following has been put on hold till followers pick up')


def update_user_status_sexaprice_api():
    print('\n')
    print('getting latest news from sexaprice.com and updating user status...', flush=True)

    print('checking remaining request count...')
    remaining = None
    try:
        remaining = api.rate_limit_status()['resources']['application']['/application/rate_limit_status']['remaining']
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    new_sites = None
    try:
        url = ('http://www.sexaprize.com/api/new.json')
        response = requests.get(url)
        new_sites = response.json()
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    if len(new_sites) > 0:
        for key, value in new_sites.items():

            try:

                if remaining > 100:
                    print('posting sexaprize link ' + value + ' update, liking and tweeting now', flush=True)
                    tweet = api.update_status(
                        'http://' + str(value) + '\n' +
                        '\n By: ' +
                        'AdultLoggs & SexaPrize' + '\n' +
                        HASH_TAGS
                    )
                    tweet.favorite()
                else:
                    print('Status update limit has been reached for now...')
                    break

            except tweepy.TweepError as e:
                if not e.api_code == 187:
                    print('Error Message: ' + get_exception_message(e.reason))
                else:
                    continue

            except StopIteration:
                break
    else:
        print('No results returned from sexaprize')


while True:

    # timeout
    timeout = 10000.0

    # following
    try:
        update_follow_followers()
    except Exception as e:
        print('Error Message: ' + str(e))

    # # timeline
    try:
        update_home_timeline()
    except Exception as e:
        print('Error Message: ' + str(e))

    # # mentions
    try:
        update_user_mentions()
    except Exception as e:
        print('Error Message: ' + str(e))

    # sexaprice_api
    try:
        update_user_status_sexaprice_api()
    except Exception as e:
        print('Error Message: ' + str(e))

    # boot
time.sleep(timeout)