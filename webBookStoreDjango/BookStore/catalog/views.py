from django.shortcuts import render
from .category import *
# tìm book by catalog
# Create your views here.
def allCategory(req):
    categories = getCategories()
    content = {
        'page_title': 'Categoies',
        'categories_book': categories["book"],
        'categories_mobile': categories["mobile"],
        'categories_clothes': categories["clothes"],
        }
    return render(req, 'catalog/categories.html', content)

def showBooksByCategory(req, id):
    category = getBookCategory(id)
    products = getBooksByCategory(id)
    content = {'products': products,
               'page_title': 'Books by ' + str(category['name']) }
    return render(req, 'product/products.html', content)

def showMobilesByCategory(req, id):
    category = getMobileCategory(id)
    products = getMobilesByCategory(id)
    content = {'products': products,
               'page_title': 'Mobiles by ' + str(category['name']) }
    return render(req, 'mobile/mobiles.html', content)

def showClothesByCategory(req, id):
    category = getClothesCategory(id)
    products = getClothesByCategory(id)
    content = {'products': products,
               'page_title': 'Clothes by ' + str(category['name']) }
    return render(req, 'clothes/clothes.html', content)
