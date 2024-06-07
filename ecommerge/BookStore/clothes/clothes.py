import requests
from json import *

def getClothesServiceUrl(url = 'http://127.0.0.1:9999/clothes/'):
    clothes = requests.get(url).json()
    if len(clothes)>0:
        return clothes
    return None

def getDetailsClothesServiceUrl(url = 'http://127.0.0.1:9999/clothes/slug/', slug=""):
    link = url + str(slug) +'/'
    clothes = requests.get(link).json()
    if len(clothes)>0:
        return clothes
    return None