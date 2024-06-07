
import requests
from json import *

def searchAll(req, query):
    query = str(query).lower()
    print(query)
    result = {}
    products = []
    url = "http://127.0.0.1:9999/books/search/" + f'?query={query}'
    products = requests.get(url).json()
    result['products'] = products

    mobiles = []
    url = "http://127.0.0.1:9999/mobiles/search/" + f'?query={query}'
    mobiles = requests.get(url).json()
    result['mobiles'] = mobiles

    clothes = []
    url = "http://127.0.0.1:9999/clothes/search/" + f'?query={query}'
    clothes = requests.get(url).json()
    result['clothes'] = clothes

    return result

def searchProduct(req, query, url="http://127.0.0.1:9999/books/search/"):
    products = []
    query = str(query).lower()
    print(query)
    url = url + f'?query={query}'
    products = requests.get(url).json()
    print(products)
    return products

def searchMobile(req, query, url="http://127.0.0.1:9999/mobiles/search/"):
    mobiles = []
    query = str(query).lower()
    print(query)
    url = url + f'?query={query}'
    mobiles = requests.get(url).json()
    print(mobiles)
    return mobiles

def searchClothes(req, query, url="http://127.0.0.1:9999/clothes/search/"):
    clothes = []
    query = str(query).lower()
    print(query)
    url = url + f'?query={query}'
    clothes = requests.get(url).json()
    print(clothes)
    return clothes

