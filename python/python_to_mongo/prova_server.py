from pymongo import MongoClient
import datetime
import pprint


client = MongoClient('localhost', 27017)
db = client.test_database

posts = db.posts
print(db);


post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}

post_id = posts.insert_one(post).inserted_id
# After inserting the first document, the posts collection has actually been created on the server.


print(post_id)
pprint.pprint(posts.find_one())
pprint.pprint(posts.find_one({"author": "Mike"}))

new_posts = [{"author": "Mike",
              "text": "Another post!",
              "tags": ["bulk", "insert"],
              "date": datetime.datetime(2009, 11, 12, 11, 14)},
             {"author": "Eliot",
              "title": "MongoDB is fun",
              "text": "and pretty easy too!",
              "date": datetime.datetime(2009, 11, 10, 10, 45)}]
result = posts.insert_many(new_posts)


for post in posts.find():
  pprint.pprint(post)
  
for post in posts.find({"author": "Mike"}):
  pprint.pprint(post)

