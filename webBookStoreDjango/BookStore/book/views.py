from django.shortcuts import render
import requests
from json import *
from .book import *


# Create your views here.
def getBooks(req):
    books = None
    while books is None:
        try:
            books = req.session['books']
        except:
            books = getBooksServiceUrl()
    content = {
        'page_title': 'books',
        'products': books
    }
    return render(req, 'product/products.html', content)

def detailsBook(req, slug):
    books = None
    while books is None:
        books = getDetailsBookServiceUrl(slug=slug)
    content = {
        'page_title': 'details book',
        'product': books
    }
    return render(req, 'product/details_product.html', content)

