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
    print("-----------------------------")
    print("Product Service: getDetailsClothesServiceUrl - " + 'http://127.0.0.1:9999/clothes/slug/')
    print("data:")
    print(clothes)
    try:
        if clothes['id'] :
            return clothes
    except:
        return None

def getClothesCategoriesServiceUrl(url = 'http://127.0.0.1:9999/clothes/types/'):
    categories = requests.get(url).json()
    if len(categories)>0:
        return categories
    return None

def getDetailsClothesCategoryServiceUrl(url = 'http://127.0.0.1:9999/clothes/types/', id=""):
    link = url + str(id) +'/'
    category = requests.get(link).json()
    try:
        if category['id'] :
            return category
    except:
        return None

def getCLothesByCategoryServiceUrl(url = 'http://127.0.0.1:9999/clothes/clothes-by-type/', id=""):
    link = url + str(id) +'/'
    clothes = requests.get(link).json()
    if len(clothes)>0:
        return clothes
    return None