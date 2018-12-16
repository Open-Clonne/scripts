import tweepy
import requests
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


def check_rate_limit_remaining():
    print('\n')
    print('checking remaining request count...')

    try:
        remaining = api.rate_limit_status()['resources']['application']['/application/rate_limit_status']['remaining']
        return remaining
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))


def update_user_mentions():
    print('\n')
    print('retrieving and replying to hash-tags...', flush=True)

    lid = retrieve_id('user_status.txt')
    if not lid:
        print('no lid found')

    try:
        check_rate_limit_remaining()
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    mentions = api.mentions_timeline(lid, tweet_mode='extended')

    for mention in reversed(mentions):
        try:

            if check_rate_limit_remaining() > 30:
                lid = mention.id
                store_id(lid, 'user_status.txt')

                if '#graytheexpert' in mention.full_text.lower():
                    print('found hash-tag and responding, liking and re-tweeting now', flush=True)
                    api.update_status(
                        '@' + mention.user.screen_name + ' good read there, thanks sir #grayTheExpert', mention.id
                    )
                    api.retweet(mention.id)
                    mention.favorite()
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

    try:
        check_rate_limit_remaining()
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    timeline = api.home_timeline(lid)

    for timeline_tweet in reversed(timeline):
        try:

            if check_rate_limit_remaining() > 50:
                print('liking and re-tweeting ' + str(timeline_tweet.id) + ' tweets in timeline now...', flush=True)

                lid = timeline_tweet.id
                store_id(lid, 'timeline.txt')

                timeline_tweet.favorite()
                timeline_tweet.retweet()
            else:
                print('Timeline likes and re-tweets exceeded for now...')

        except tweepy.TweepError as e:
            print('Error Message: ' + get_exception_message(e.reason))

        except StopIteration:
            break


def update_follow_followers():
    print('\n')
    print('following all new followers...', flush=True)

    try:
        check_rate_limit_remaining()
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    user = api.me()
    followers = api.followers(user.id)

    if (user.friends_count < 1000) and (user.followers_count + 500) < 1000:
        for follower in reversed(followers):
            try:
                if not follower.following:
                    if follower.id == user.id:
                        print('Not following self, passing on...')
                        continue
                    else:
                        if check_rate_limit_remaining() > 160:
                            follower.follow()
                            print("Followed everyone that is following " + user.name)
                        else:
                            print('Follow limit exceeded, no more following for now')
                            break
                else:
                    if check_rate_limit_remaining() > 160:
                        print('All following has been completed and none found so finding user followers')
                        find_user_followers(follower.id)
                    else:
                        print('Follow limit exceeded, no more following for now')
                        break

            except tweepy.TweepError as e:
                print('Error Message: ' + get_exception_message(e.reason))

            except StopIteration:
                break
    else:
        print('Following has been put on hold till followers pick up')


def find_user_followers(follower_id):
    print('\n')
    print('Finding user and followers and following them')

    try:
        check_rate_limit_remaining()
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    f_user = api.get_user(follower_id)
    user = api.me()

    f_followers = api.followers(follower_id)

    if (user.friends_count < 1000) and (user.followers_count + 500) < 1000:
        i = 10
        for i, follower in enumerate(f_followers):
            try:
                if (user.friends_count < 1000) and (user.followers_count + 500) < 1000:
                    print('Following has been put on hold till followers pick up')
                    break

                if follower.following:
                    print('Already following ' + follower.name + ' so moving on...')
                    continue
                else:
                    if follower.id == f_user.id:
                        print('Not following self, passing on...')
                        continue
                    else:
                        if check_rate_limit_remaining() > 160:
                            follower.follow()
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
                if check_rate_limit_remaining() > 100:
                    print('saving new lid now')
                    store_id(lid, 'hacker_news.txt')
                    print('hacker_news top story, responding, liking and re-tweeting now', flush=True)

                    tweet = api.update_status(
                        str(story.title) + '\n' + str(story.url) + '\n By: ' + str(story.by) + '\n' + '#hackernews' + '\n' + CLONNEBOTS
                    )
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

    url = ('https://newsapi.org/v2/top-headlines?country=us&apiKey=' + NEWS_API_KEY)
    response = requests.get(url)
    top_headlines = response.json()

    if top_headlines['status'] == 'ok':
        for headline in top_headlines['articles']:
            try:

                if check_rate_limit_remaining() > 100:
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
    update_follow_followers()
    update_user_status_hacker_news()
    update_user_status_news_api()
    update_user_mentions()
    update_home_timeline()

    for minutes in range(0, 59):
        if minutes not in {0, 15, 30, 45}:
            snooze = 15 - minutes % 15
            print('minutes:', minutes, ' sleep({}):'.format(snooze * 60))
        else:
            print('minutes:', minutes, ' no sleep')
