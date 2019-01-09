import os
import time
import tweepy
from keys import *
from gtts import gTTS
from pygame import mixer


print('\n')
print('booting up reporterBot', flush=True)


# grayTheExpert
gray_auth = tweepy.OAuthHandler(GRAY_CONSUMER_KEY, GRAY_CONSUMER_SECRET)
gray_auth.set_access_token(GRAY_ACCESS_KEY, GRAY_ACCESS_SECRET)
gray_api = tweepy.API(gray_auth)


# jonesTheExpert
jones_auth = tweepy.OAuthHandler(JONES_CONSUMER_KEY, JONES_CONSUMER_SECRET)
jones_auth.set_access_token(JONES_ACCESS_KEY, JONES_ACCESS_SECRET)
jones_api = tweepy.API(jones_auth)


# linusTheExpert
lin_auth = tweepy.OAuthHandler(LIN_CONSUMER_KEY, LIN_CONSUMER_SECRET)
lin_auth.set_access_token(LIN_ACCESS_KEY, LIN_ACCESS_SECRET)
lin_api = tweepy.API(lin_auth)


def delete_audio(file_name):
    if os.path.exists(file_name):
        print('Deleting old audio file now')
        os.remove(file_name)
    else:
        print('No audio file found')


def retrieve_f_store(file_name):
    f_read = open(file_name, 'r')
    lid = int(f_read.read().strip())
    f_read.close()
    return lid


def store_f(fid, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(fid))
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


def gray_followers():
    print('\n')
    print('grayTheExpert followers...', flush=True)

    fid = retrieve_f_store('gray_f.txt')
    if not str(fid):
        print('no fid found')

    print('checking remaining request count...')
    try:
        remaining = gray_api.rate_limit_status()['resources']['application']['/application/rate_limit_status']['remaining']
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    followers = None
    try:
        user = user = gray_api.me()
        followers = user.followers_count

        print('calculating follow difference')
        increase = None
        decrease = None
        if followers < fid:
            decrease = fid - followers
        else:
            decrease = 0

        if followers > fid:
            increase = followers - fid
        else:
            increase = 0

        msg = None
        if increase == 0 and decrease >= 0:
            msg = 'great work guys!!!'
        else:
            msg = 'Hurray!!!.'

        delete_audio('gray_f.mp3')

        print('announcing current followers in female voice now')
        print('compiling and saving audio file now')
        tts = gTTS(str(user.screen_name) + ' currently has ' + 
                str(followers) + ' followers, with ' + str(increase) + 
                ' increase and ' + str(decrease) + ' decrease as at now, ' + 
                msg, 'en', False, True, [])
        tts.save('gray_f.mp3')

        print('playing audio file now')
        mixer.init()
        mixer.music.load('gray_f.mp3')
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(1)
            print('still playing audio')

        print('quit audio player now')
        mixer.quit()

        print('storing current follower count')
        store_f(followers, 'gray_f.txt')

        print ("All done now")

    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))


def jones_followers():
    print('\n')
    print('jonesTheExpert followers...', flush=True)

    fid = retrieve_f_store('jones_f.txt')
    if not str(fid):
        print('no fid found')

    print('checking remaining request count...')
    try:
        remaining = jones_api.rate_limit_status()['resources']['application']['/application/rate_limit_status']['remaining']
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    followers = None
    try:
        user = user = jones_api.me()
        followers = user.followers_count

        print('calculating follow difference')
        increase = None
        decrease = None
        if followers < fid:
            decrease = fid - followers
        else:
            decrease = 0

        if followers > fid:
            increase = followers - fid
        else:
            increase = 0

        msg = None
        if increase == 0 and decrease >= 0:
            msg = 'great work guys!!!'
        else:
            msg = 'Hurray!!!.'

        delete_audio('jones_f.mp3')

        print('announcing current followers in female voice now')
        print('compiling and saving audio file now')
        tts = gTTS(str(user.screen_name) + ' currently has ' + 
                str(followers) + ' followers, with ' + str(increase) + 
                ' increase and ' + str(decrease) + ' decrease as at now, ' + 
                msg, 'en', False, True, [])
        tts.save('jones_f.mp3')

        print('playing audio file now')
        mixer.init()
        mixer.music.load('jones_f.mp3')
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(1)
            print('still playing audio')

        print('quit audio player now')
        mixer.quit()

        print('storing current follower count')
        store_f(followers, 'jones_f.txt')

        print ("All done now")

    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))


def lin_followers():
    print('\n')
    print('linusTheExpert followers...', flush=True)

    fid = retrieve_f_store('lin_f.txt')
    if not str(fid):
        print('no fid found')

    print('checking remaining request count...')
    try:
        remaining = lin_api.rate_limit_status()['resources']['application']['/application/rate_limit_status']['remaining']
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    followers = None
    try:
        user = user = lin_api.me()
        followers = user.followers_count

        print('calculating follow difference')
        increase = None
        decrease = None
        if followers < fid:
            decrease = fid - followers
        else:
            decrease = 0

        if followers > fid:
            increase = followers - fid
        else:
            increase = 0

        msg = None
        if increase == 0 and decrease >= 0:
            msg = 'great work guys!!!'
        else:
            msg = 'Hurray!!!.'

        delete_audio('lin_f.mp3')

        print('announcing current followers in female voice now')
        print('compiling and saving audio file now')
        tts = gTTS(str(user.screen_name) + ' currently has ' + 
                str(followers) + ' followers, with ' + str(increase) + 
                ' increase and ' + str(decrease) + ' decrease as at now, ' + 
                msg, 'en', False, True, [])
        tts.save('lin_f.mp3')

        print('playing audio file now')
        mixer.init()
        mixer.music.load('lin_f.mp3')
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(1)
            print('still playing audio')

        print('quit audio player now')
        mixer.quit()

        print('storing current follower count')
        store_f(followers, 'lin_f.txt')

        print ("All done now")

    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))


while True:

    # timeout
    timeout = 100.0

    # grayTheExpert followers
    try:
        gray_followers()
    except Exception as e:
        print('Error Message: ' + str(e))

    # boot
    time.sleep(timeout)

    # jonesTheExpert followers
    try:
        jones_followers()
    except Exception as e:
        print('Error Message: ' + str(e))

    # boot
    time.sleep(timeout)

    # linTheExpert followers
    try:
        lin_followers()
    except Exception as e:
        print('Error Message: ' + str(e))

    # boot
    time.sleep(timeout)
