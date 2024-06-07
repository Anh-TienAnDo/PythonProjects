import requests
from json import *

def getBooksServiceUrl(url = 'http://127.0.0.1:9999/books/'):
    books = requests.get(url).json()
    if len(books)>0:
        return books
    return None

# lấy chi tiết 1 book
def getDetailsBookServiceUrl(url = 'http://127.0.0.1:9999/books/slug/', slug=""):
    link = url + str(slug) +'/'
    book = requests.get(link).json()
    print("-----------------------------")
    print("Product Service: getDetailsBookServiceUrl - " + 'http://127.0.0.1:9999/books/slug/')
    print("data:")
    print(book)
    try:
        if book['id'] :
            return book
    except:
        return None

# lấy những category 
def getBookCategoriesServiceUrl(url = 'http://127.0.0.1:9999/books/categories/'):
    categories = requests.get(url).json()
    if len(categories)>0:
        return categories
    return None

# lấy chi tiết 1 category 
def getDetailsBookCategoryServiceUrl(url = 'http://127.0.0.1:9999/books/categories/', id=""):
    link = url + str(id) +'/'
    category = requests.get(link).json()
    try:
        if category['id'] :
            return category
    except:
        return None

# lấy book theo cate 
def getBooksByCategoryServiceUrl(url = 'http://127.0.0.1:9999/books/books-by-category/', id=""):
    link = url + str(id) +'/'
    books = requests.get(link).json()
    if len(books)>0:
        return books
    return None