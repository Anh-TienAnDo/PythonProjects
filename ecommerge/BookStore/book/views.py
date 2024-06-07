from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from mongodb_connection import db
from bson.objectid import ObjectId
from pymongo import ASCENDING

book_table = db.books
author_table = db['authors']
category_table = db['categories']
publisher_table = db['publishers']


def addID(datas):
    result = []
    for data in datas:
        data['id'] = str(data['_id'])
        result.append(data)
    return result

# Create your views here
def allBook(req):
    books = book_table.find({}) # get all documents
    books_idstr = []
    for book in books:
        book['id'] = str(book['_id']) # type dict
        books_idstr.append(book)
    count = book_table.count_documents({})
    content = {
        'books': books_idstr,
        'count': count,
    }
    return render(req, 'book/books.html', content)

def searchBooks(req):
    query = req.GET.get('keyword')
    if query:
        books = db.books.find({'title': {'$regex': query, '$options': 'i'}})
    else:
        books = db.books.find()
    context = {
        'books': books,
        'query': query,
    }

    return render(req, 'book/search_books.html', context)

def detailsBook(req, book_id):
    book = book_table.find_one({'_id': ObjectId(book_id)})
    authors = []
    categories = []
    for author_id in book["authors"]:
        author = author_table.find_one({'_id': author_id})
        authors.append(author)
    for category_id in book["categories"]:
        category = category_table.find_one({'_id': category_id})
        categories.append(category)
    publisher = publisher_table.find_one({'_id': book['publisher']})
    content = {
        'book': book,
        'authors': authors,
        'categories': categories,
        'publisher': publisher,
    }
    return render(req, 'book/details_book.html', content)

def addBook(req):
    authors = addID(author_table.find({}))
    publisher = addID(publisher_table.find({}))
    categories = addID(category_table.find({}))

    content = {
        'authors': authors,
        'categories': categories,
        'publisher': publisher,
    }
    if req.method == 'POST':
        title = req.POST.get('title')
        author_ids = [ObjectId(id) for id in req.POST.getlist('authors')]
        category_ids = [ObjectId(id) for id in req.POST.getlist('categories')]
        publisher_id = ObjectId(req.POST.get('publisher'))

        check_dup = book_table.find_one({'title': title})
        if check_dup is None:
            book = Book(title=title, authors=author_ids, publisher=publisher_id, categories=category_ids)
            result = book.save()
            messenger = 'Add success'
        else:
            messenger = "Error existed title"
        content['messenger'] = messenger

        return render(req, 'book/add_book.html', content)


    return render(req, 'book/add_book.html', content)


def test(req):
    authors = addID(author_table.find({}))
    publisher = addID(publisher_table.find({}))
    categories = addID(category_table.find({}))

    content = {
        'authors': authors,
        'categories': categories,
        'publisher': publisher,
    }
    if req.method == 'POST':
        title = req.POST.get('title')
        author_ids = req.POST.getlist('authors')
        category_ids = req.POST.getlist('categories')
        publisher_id = req.POST.get('publisher')

        return HttpResponse(len(author_ids))


    return render(req, 'book/add_book.html', content)
