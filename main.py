# -*- coding: utf-8 -*-

from tweepy import *
import os
import json
import urllib
import datetime
import argparse
import pymongo

parser = argparse.ArgumentParser(description='Twitter Saver')
parser.add_argument('--config', '-c', required=True, type=str, help='config path')
parser.add_argument('--list', '-l', required=True, type=str, help='user list path')
args = parser.parse_args()

def get_oauth():
    with open(args.config, 'rb') as f:
        data = f.read()
    f.close()
    lines = data.split('\n')
    consumer_key = lines[0]
    consumer_secret = lines[1]
    access_key = lines[2]
    access_secret = lines[3]
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return auth

def get_userlist():
    with open(args.list, 'rb') as l:
        lines = l.readlines()
    l.close()
    return lines

def set_database():
    # Connection MongoDB
    client = pymongo.MongoClient('localhost', 27017)
    # Select Databse
    db = client.save_tweets
    # Return Collection
    return db.tweets

class StreamListener(StreamListener):
    def on_status(self, status):
        if not status.entities.has_key('retweeted_status'):
            for line in lines:
                if line.find(status.author.screen_name) >= 0:

                    # text save
                    try:
                        print u"{0}@{1}".format(status.author.screen_name, status.text)
                        tweet_json = status._json
                        co.insert_one(tweet_json)
                    except Exception as e:
                        print e
                        pass

                    # image save
                    if status.entities.has_key('media'):
                        medias = status.entities['media']
                        m = medias[0]
                        media_url = m['media_url']
                        print u"MediaURL : {0}".format(media_url)
                        now = datetime.datetime.now()
                        time = now.strftime("%H%M%S")
                        filedir = './download/{}'.format(status.author.screen_name)
                        try:
                            os.makedirs(filedir)
                        except OSError:
                            pass
                        filename = os.path.join(filedir, '{}.jpg'.format(status.id))
                        print u"Save File : {0}".format(filename)
                        try:
                            urllib.urlretrieve(media_url, filename)
                        except IOError:
                            print "Image Save Failed : {0}".format(media_url)

                    print "\n"

    def on_timeout(self):
        return True

auth = get_oauth()
lines = get_userlist()
co = set_database()
stream = Stream(auth, StreamListener(), secure = True)
print "Start Streaming!"
try:
    os.makedirs('./download')
except:
    pass
stream.userstream()
