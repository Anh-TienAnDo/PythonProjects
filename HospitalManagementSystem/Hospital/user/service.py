import requests
from json import *
from django.shortcuts import render, redirect

class Person:
    def __init__(self):
        pass

    def login(self, url='http://127.0.0.1:9997/user/login/', data={}):
        user = requests.post(url, json=data).json()
        return user
    
    def get_user(self, url='http://127.0.0.1:9997/user/', id=1):
        user = requests.get(url + str(id)).json()
        return user

