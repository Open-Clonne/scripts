import os
import time
import tweepy
import pyttsx3
from keys import *
from pygame import mixer

print('\n')
print('booting up reporterBot[Twitter]', flush=True)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


def delete_audio():
    if os.path.exists("follow.mp3"):
        print('Deleting old audio file now')
        os.remove('follow.mp3')
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


def get_follower_count_reporter():
    print('\n')
    print('retrieving and announcing current followers...', flush=True)

    fid = retrieve_f_store('followers.txt')
    if not str(fid):
        print('no fid found')

    print('checking remaining request count...')
    remaining = None
    try:
        remaining = api.rate_limit_status()['resources']['application']['/application/rate_limit_status']['remaining']
    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))

    followers = None
    try:
        user = user = api.me()
        followers = user.followers_count

        print('storing current follower count')
        store_f(followers, 'followers.txt')

        if followers >= fid:
            print('calculating follow difference')
            prev_f = followers - fid

            msg = None
            if prev_f == 0:
                msg = 'do not worry it will pick up soon.'

                delete_audio()

                print('announcing current followers in female voice now')
                print('compiling and saving audio file now')
                tts = gTTS(str(user.screen_name) + ' currently has ' + 
                    str(followers) + ' followers, with ' + str(prev_f) + 
                    ' increase as at now, ' + msg, 'en', False, True, [])
                tts.save('follow.mp3')

                print('playing audio file now')
                mixer.init()
                mixer.music.load('follow.mp3')
                mixer.music.play()
                while mixer.music.get_busy():
                    time.sleep(1)
                    print('still playing audio')

                print('quit audio player now')
                mixer.quit()
                delete_audio()

                print ("All done now")
            else:
                msg = 'Hurray!!!.'

                delete_audio()

                print('announcing current followers in female voice now')
                print('compiling and saving audio file now')
                tts = gTTS(str(user.screen_name) + ' currently has ' + 
                    str(followers) + ' followers, with ' + str(prev_f) + 
                    ' increase as at now, ' + msg, 'en', False, True, [])
                tts.save('follow.mp3')

                print('playing audio file now')
                mixer.init()
                mixer.music.load('follow.mp3')
                mixer.music.play()
                while mixer.music.get_busy():
                    time.sleep(1)
                    print('still playing audio')

                print('quit audio player now')
                mixer.quit()
                delete_audio()

                print ("All done now")

    except tweepy.TweepError as e:
        print('Error Message: ' + get_exception_message(e.reason))


while True:

    # timeout
    timeout = 100.0

    # followers count reporter
    try:
        get_follower_count_reporter()
    except Exception as e:
        print('Error Message: ' + str(e))

    # boot
    time.sleep(timeout)
