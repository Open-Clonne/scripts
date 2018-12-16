import tweepy
import requests
from keys import *
from hackernews import HackerNews
from twisted.internet import task, reactor

print('booting up clonneBot[Grayson]', flush=True)

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

    print('checking remaining request count...')
    try:
        remaining = api.rate_limit_status()['resources']['application']['/application/rate_limit_status']['remaining']
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

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
                        '@' + mention.user.screen_name + ' good read there, thanks sir #grayTheExpert', mention.id
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
    try:
        remaining = api.rate_limit_status()['resources']['application']['/application/rate_limit_status']['remaining']
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

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

    followers = []
    user = []
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


def update_user_status_hacker_news():
    print('\n')
    print('getting latest news from hacker_news and updating user status...', flush=True)

    print('checking remaining request count...')
    try:
        remaining = api.rate_limit_status()['resources']['application']['/application/rate_limit_status']['remaining']
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    try:
        hn = HackerNews()
        stories = hn.top_stories(limit=15)
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    for story in stories:
        try:

            lid_r = retrieve_id('hacker_news.txt')

            lid = story.item_id

            if lid > lid_r:
                if remaining > 100:
                    print('hacker_news top story, responding, liking and re-tweeting now', flush=True)

                    tweet = api.update_status(
                        str(story.title) + '\n' + str(story.url) + '\n By: ' + str(story.by) + '\n' + '#hackernews' + '\n' + CLONNEBOTS
                    )

                    print('saving new lid now')
                    store_id(lid, 'hacker_news.txt')

                    tweet.retweet()
                    tweet.favorite()
                else:
                    print('Status update limit has been reached for now...')
                    break
            else:
                print('no new top stories are available at this time', flush=True)

        except tweepy.TweepError as e:
            print('Error Message: ' + get_exception_message(e.reason))

        except StopIteration:
            break


def update_user_status_news_api():
    print('\n')
    print('getting latest news from news_api and updating user status...', flush=True)

    print('checking remaining request count...')
    try:
        remaining = api.rate_limit_status()['resources']['application']['/application/rate_limit_status']['remaining']
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    try:
        url = ('https://newsapi.org/v2/top-headlines?country=us&apiKey=' + NEWS_API_KEY)
        response = requests.get(url)
        top_headlines = response.json()
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    if top_headlines['status'] == 'ok':
        for headline in top_headlines['articles']:
            try:

                if remaining > 100:
                    print('news_api top story, responding, liking and re-tweeting now', flush=True)
                    tweet = api.update_status(
                        str(headline['title']) + '\n' +
                        str(headline['url']) + '\n By: ' +
                        str(headline['source']['name']) + '\n' +
                        '#newsapi' + '\n' +
                        CLONNEBOTS
                    )
                    tweet.retweet()
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
        print('Could not get top_headlines from news_api')


while True:
    # 15 minutes
    timeout = 500.0

    # following
    try:
        follow_followers = task.LoopingCall(update_follow_followers())
        follow_followers.start(timeout)
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    # timeline
    try:
        home_timeline = task.LoopingCall(update_home_timeline())
        home_timeline.start(timeout)
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    # mentions
    try:
        mentions = task.LoopingCall(update_user_mentions())
        mentions.start(timeout)
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    # hacker_news
    try:
        hacker_news = task.LoopingCall(update_user_status_hacker_news())
        hacker_news.start(timeout)
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    # news_api
    try:
        news_api = task.LoopingCall(update_user_status_news_api())
        news_api.start(timeout)
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    # boot
    try:
        reactor.run()
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))
