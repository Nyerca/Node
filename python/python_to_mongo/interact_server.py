from pymongo import MongoClient
import datetime
import pprint

client = MongoClient('localhost', 27017)
db = client.test_database

posts = db.posts
print(db);

posts.remove({'author':"Mike"});

for post in posts.find():
  pprint.pprint(post)