import json

import requests
from json import *
from bs4 import BeautifulSoup as bs
from selenium import webdriver # web: html + css + javasricpt
from selenium.webdriver.common.keys import Keys #Keys: cung cấp các phím trên bàn phím
from selenium.webdriver.common.by import By # By: định vị các thành phần trong tài liệu.
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import jwt, datetime

# m = {'a':1, 'b':2}
# m2 = {'c':3, 'b':4}
# m.update(m2)
# m3 = m
# print(m3)
# print(datetime.datetime.utcnow() + datetime.timedelta(minutes=30))
# print(datetime.datetime.now())

url = 'http://127.0.0.1:9995/notification/email'
data = {
    'user_id': 1,
    'name': 'anhle',
    'phone': '123123123',
    'email': 'lea81807@gmail.com',
    'address': 'ha dong',
    'city': 'ha noi',
    'code': 'asdfasdf',
}
response = requests.post(url, json=data)
response = response.json()
print(response)

# url = 'http://127.0.0.1:9997/user/login'
# headers = {
#     'Content-Type': 'application/json',  # Example header
#     'Authorization': 'Bearer YOUR_TOKEN', # Example header for authorization
# }
#
# # Define the data to send in the request (optional)
# data = {
#     'username': 'anhgdt',
#     'password': 'Song3goc',
# }
#
#
# # Make the POST request with headers and data
# response = requests.post(url, headers=headers, json=data)
# response = response.json()
# print(response)
# d = response.get('data')
# print(d)
# token = d.get('token')
# payload = jwt.decode(jwt=token, key='BAT_CHANH_DAO', algorithms=['HS256'])
# print(payload)

# url = 'http://127.0.0.1:9997/user/register'
# url = 'http://127.0.0.1:9995/carts/api/1/create'

# url = 'http://127.0.0.1:9995/payment/api/create_or_update'
# payment_data = {
#                     'checkout_id': 8,
#                     'code': '5b1A7l0KQg',
#                     'bank': '0',
#                     'total': 320000,
#                 }
# response = requests.post(url, json=payment_data)
# print(response.json())

# url = 'http://127.0.0.1:9995/orders/api/checkouts/2'
# response = requests.get(url).json()
# print(response)

# url = 'http://127.0.0.1:9995/orders/api/checkouts/1/ffP0ehRwGZ/cancel'
# response = requests.get(url).json()
# print(response)

# url = 'http://127.0.0.1:9995/orders/api/order-items/4'
# open it, go to a website, and get results

# url = 'http://127.0.0.1:9997/admin/login/?next=/admin/'
# wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# wd.get(url)
#
# # Điền thông tin vào form
# username_input = wd.find_element(By.NAME, 'username')
# username_input.send_keys('anhgdt')
#
# password_input = wd.find_element(By.NAME, 'password')
# password_input.send_keys('Song3goc')
#
# # Submit form
# password_input.send_keys(Keys.ENTER)
# url = 'http://127.0.0.1:9997/admin/user_model/user/'
# wd.get(url)
# html_doc = wd.page_source
# soup = bs(html_doc, 'html.parser')
# # print(soup)
#
# content = soup.find('div', {"class": "content"})
# print(content)

# wd.quit()
# form_tab = soup.find('form', {"data-test-id": "pin-visual-wrapper"}))
# print(response.text)

# data={'user_id': 1,
#       'product_slug': "co-hoc-tinh-hoa",
#       'quantity': 2}
# response = requests.post(product_service_url, json=data)
# response = response.json()
# print(response)
# print(type(response))






# data = {
#     'username': 'leanh',
#     'password': 'Song3goc',
#     'email': 'leanh@gmail.com',
#     'fname': 'anh',
#     'lname': 'le hong',
#     'phone': '0123456789',
#     'street': '123 Main St',
#     'district': 'Downtown',
#     'city': 'Example City',
# }


# number = 3580000
# formatted_number = "{:,.0f}".format(number)
# print(formatted_number)  # Output: 3.580.000

# d = [{'n':'a', 's':'a'}, {'n':'a2', 's':'a2'}, {'n':'a3', 's':'a4'}]
# from fuzzywuzzy import fuzz
# r = fuzz.partial_ratio('le h', 'le hong anh')
# print(r)




















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