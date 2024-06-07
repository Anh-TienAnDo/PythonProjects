import requests
from json import *
from book.book import *
from mobile.mobile import *
from clothes.clothes import *


def getCategories():
    categories = {}
    categories['book'] = getBookCategoriesServiceUrl()
    categories['mobile'] = getMobileCategoriesServiceUrl()
    categories['clothes'] = getClothesCategoriesServiceUrl()
    return categories

def getBooksByCategory(id):
    return getBooksByCategoryServiceUrl(id=str(id))

def getBookCategory(id):
    return getDetailsBookCategoryServiceUrl(id=str(id))

def getMobilesByCategory(id):
    return getMobilesByCategoryServiceUrl(id=str(id))

def getMobileCategory(id):
    return getDetailsMobileCategoryServiceUrl(id=str(id))

def getClothesByCategory(id):
    return getCLothesByCategoryServiceUrl(id=str(id))

def getClothesCategory(id):
    return getDetailsClothesCategoryServiceUrl(id=str(id))

