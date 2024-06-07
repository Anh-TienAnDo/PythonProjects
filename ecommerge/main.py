import requests
from json import *

producers_service_url = 'http://127.0.0.1:9999/clothes/1/'
response = requests.get(producers_service_url)
print(type(response.json()))
print(response.json())
# print(type(response.json()[0]))
print(len(response.json()))

# for r in response.json():
#     print(r['name'])
# print(type(response.text))
# print(response.status_code)

# from BookStore.catalog.models import *
# products = Category.objects.all()
# print(type(products))
# print(products[0][name])
# print(products)

# import pymongo
#
#
# url = 'mongodb://localhost:27017'
# client = pymongo.MongoClient(url)
# #
# db = client['bookstore']
#
# user_table = db.users
#
# documents = [
#     {'name': 'user1', 'email': 'user1@gmail.com', 'phone': '123456789'},
#     {'name': 'user2', 'email': 'user2@gmail.com', 'phone': '987654321', 'address': 'hanoi'}
# ]
# user_table.insert_many(documents)

# user_table.update_one({'name': 'user1'}, {'$set':{'phone':'192837465'}})
# user_table.delete_one({'name': 'user1'})
# for user in user_table.find():
#     print(user)
# user_table.drop()
# print('tables collection:', db.list_collection_names())









# insert_one(post).inserted_id
# insert_many(new_posts).inserted_ids

# result = db.profiles.create_index([("user_id", pymongo.ASCENDING)], unique=True)
# sorted(list(db.profiles.index_information()))
# ['_id_', 'user_id_1']
#
# user_profiles = [{"user_id": 211, "name": "Luke"}, {"user_id": 212, "name": "Ziltoid"}]
# result = db.profiles.insert_many(user_profiles)
#
# new_profile = {"user_id": 213, "name": "Drew"}
# duplicate_profile = {"user_id": 212, "name": "Tommy"}
# result = db.profiles.insert_one(new_profile)  # This is fine.
# result = db.profiles.insert_one(duplicate_profile)