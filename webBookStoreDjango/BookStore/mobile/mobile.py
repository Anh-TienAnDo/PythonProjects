import requests
from json import *

def getMobilesServiceUrl(url = 'http://127.0.0.1:9999/mobiles/'):
    mobiles = requests.get(url).json()
    if len(mobiles)>0:
        return mobiles
    return None

def getDetailsMobileServiceUrl(url = 'http://127.0.0.1:9999/mobiles/slug/', slug=""):
    link = url + str(slug) +'/'
    mobile = requests.get(link).json()
    print("-----------------------------")
    print("Product Service: getDetailsMobileServiceUrl - " + 'http://127.0.0.1:9999/mobiles/slug/')
    print("data:")
    print(mobile)
    try:
        if mobile['id'] :
            return mobile
    except:
        return None

def getMobileCategoriesServiceUrl(url = 'http://127.0.0.1:9999/mobiles/types/'):
    categories = requests.get(url).json()
    if len(categories)>0:
        return categories
    return None

def getDetailsMobileCategoryServiceUrl(url = 'http://127.0.0.1:9999/mobiles/types/', id=""):
    link = url + str(id) +'/'
    category = requests.get(link).json()
    try:
        if category['id'] :
            return category
    except:
        return None

def getMobilesByCategoryServiceUrl(url = 'http://127.0.0.1:9999/mobiles/mobiles-by-type/', id=""):
    link = url + str(id) +'/'
    mobiles = requests.get(link).json()
    if len(mobiles)>0:
        return mobiles
    return None
