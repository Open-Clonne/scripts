import os
import time
import tweepy
from keys import *
from gtts import gTTS
from pygame import mixer


print('\n')
print('booting up reporterBot', flush=True)


# credentials
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


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


def followers():
    print('\n')
    print('getting followers...', flush=True)

    fid = retrieve_f_store('c_f.txt')
    if not str(fid):
        print('no fid found')

    print('checking remaining request count...')
    try:
        remaining = api.rate_limit_status()['resources']['application']['/application/rate_limit_status']['remaining']
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    followers = None
    try:
        if remaining > 10:
            user = user = api.me()
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

            delete_audio('c_f.mp3')

            print('announcing current followers in female voice now')
            print('compiling and saving audio file now')
            tts = gTTS(str(user.screen_name) + ' currently has ' + 
                    str(followers) + ' followers, with ' + str(increase) + 
                    ' increase and ' + str(decrease) + ' decrease as at now, ' + 
                    msg, 'en', False, True, [])
            tts.save('c_f.mp3')

            print('playing audio file now')
            mixer.init()
            mixer.music.load('c_f.mp3')
            mixer.music.play()
            while mixer.music.get_busy():
                time.sleep(1)
                print('still playing audio')

            print('quit audio player now')
            mixer.quit()

            print('storing current follower count')
            store_f(followers, 'c_f.txt')

            print ("All done now")
        else:
            print('Limit reached for now...')

    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))


while True:

    # timeout(10min)
    timeout = 200.0

    # followers
    try:
        followers()
    except Exception as e:
        print('Error Message: ' + str(e))

    # boot
    time.sleep(timeout)
