import pymongo
import json

c = pymongo.MongoClient('localhost', 27017)
d = c.save_tweets
l = d.tweets

#print l.find_one()

for data in l.find({}, {'text': 1, 'user': 1}):
    print(u"{0}@{1}").format(data["user"]["screen_name"], data["text"])

#for data in l.find({}):
    #print(u"{0}\n").format(data)
