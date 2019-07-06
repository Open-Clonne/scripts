import time
import tweepy
from keys import (
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_KEY,
    ACCESS_SECRET,
    HASH_TAGS,
    MENTION_ID
)

print('booting up twitter', flush=True)

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
        remaining = api.rate_limit_status()['resources'][
            'application'
            ][
                '/application/rate_limit_status'
            ][
                'remaining'
            ]
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    mentions = None
    try:
        if lid == 0:
            mentions = api.mentions_timeline(None, tweet_mode='extended')
        else:
            mentions = api.mentions_timeline(lid, tweet_mode='extended')
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))
    for mention in reversed(mentions):
        try:

            if remaining > 30:

                if MENTION_ID in mention.full_text.lower():
                    print(
                        'found hash-tag and responding, ' +
                        'liking and re-tweeting now',
                        flush=True
                    )

                    api.update_status(
                        '@' + mention.user.screen_name + ' great! ' +
                        HASH_TAGS, mention.id
                    )
                    api.retweet(mention.id)
                    mention.favorite()
                else:
                    print(
                        'no hash-tag found so responding, ' +
                        'liking and re-tweeting now',
                        flush=True
                    )
                    api.update_status(
                        '@' + mention.user.screen_name + ' good read! ' +
                        HASH_TAGS, mention.id
                    )
                    api.retweet(mention.id)
                    mention.favorite()

                lid = mention.id
                store_id(lid, 'user_status.txt')

            else:
                print(
                    'User mention respond, ' +
                    'liking and re-tweeting exceeded for now...'
                )

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
        remaining = api.rate_limit_status()['resources']['application'][
            '/application/rate_limit_status'
        ]['remaining']
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    timeline = None
    try:
        if lid == 0:
            timeline = api.home_timeline()
        else:
            timeline = api.home_timeline(lid)
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    for timeline_tweet in reversed(timeline):
        try:

            if remaining > 50:
                print(
                    'liking and re-tweeting ' +
                    str(timeline_tweet.id) +
                    ' tweets in timeline now...',
                    flush=True
                )

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
        remaining = api.rate_limit_status()['resources']['application'][
            '/application/rate_limit_status'
        ]['remaining']
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    followers = None
    user = None
    try:
        user = api.me()
        followers = api.followers(user.id)
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    if (user.friends_count < 1000) and (user.followers_count < 5000):
        for follower in reversed(followers):
            try:
                if not follower.following:
                    if follower.id == user.id:
                        print('Not following self, passing on...')
                        continue
                    else:
                        if remaining > 160:
                            follower.follow()
                            print(
                                "Followed everyone that is following " +
                                user.name
                            )
                        else:
                            print(
                                'Follow limit exceeded, ' +
                                'no more following for now'
                            )
                            break
                else:
                    if remaining > 160:
                        print(
                            'All following has been ' +
                            'completed and none found ' +
                            'so finding user followers'
                        )

                        print('\n')
                        print('Finding user and followers and following them')

                        f_user = None
                        try:
                            f_user = api.get_user(follower.id)
                        except tweepy.TweepError as e:
                            print(
                                'Error Message: ' +
                                get_exception_message(e.reason)
                            )

                        f_followers = api.followers(follower.id)
                        friends_count = (user.friends_count < 1000)
                        follower_count = (user.followers_count < 5000)
                        if friends_count and follower_count:

                            for f_follower in reversed(f_followers):
                                try:
                                    fri_count = user.friends_count < 1000
                                    foll_count = user.followers_count < 5000
                                    if fri_count and foll_count:
                                        print(
                                            'Following has been put on hold ' +
                                            'till followers pick up'
                                        )
                                        break

                                    if f_follower.following:
                                        print(
                                            'Already following ' +
                                            f_follower.name +
                                            ' so moving on...'
                                        )
                                        continue
                                    else:
                                        if f_follower.id == f_user.id:
                                            print(
                                                'Not following self, ' +
                                                'passing on...'
                                            )
                                            continue
                                        else:
                                            if remaining > 160:
                                                f_follower.follow()
                                                print(
                                                    "Followed " +
                                                    "everyone that " +
                                                    "is following " +
                                                    f_user.name
                                                )
                                            else:
                                                print(
                                                    'Follow limit exceeded, ' +
                                                    'no more following for now'
                                                )
                                                break

                                except tweepy.TweepError as e:
                                    print(
                                        'Error Message: ' +
                                        get_exception_message(e.reason)
                                    )

                                except StopIteration:
                                    break
                        else:
                            print(
                                'Following has been put ' +
                                'on hold till followers pick up'
                            )

                    else:
                        print(
                            'Follow limit exceeded, ' +
                            'no more following for now'
                        )
                        break

            except tweepy.TweepError as e:
                print('Error Message: ' + get_exception_message(e.reason))

            except StopIteration:
                break
    else:
        print('Following has been put on hold till followers pick up')


# loop and run
while True:

    # timeout (5min)
    timeout = time.time() + 60*180

    # following
    try:
        update_follow_followers()
    except Exception as e:
        print('Error Message: ' + str(e))

    # timeline
    try:
        update_home_timeline()
    except Exception as e:
        print('Error Message: ' + str(e))

    # mentions
    try:
        update_user_mentions()
    except Exception as e:
        print('Error Message: ' + str(e))

    # boot
    time.sleep(timeout)
