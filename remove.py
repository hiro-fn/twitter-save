import pymongo

c = pymongo.MongoClient('localhost', 27017)
d = c.save_tweets
l = d.tweets

l.remove({'test': '1'})
