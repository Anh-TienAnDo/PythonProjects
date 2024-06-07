from django.db import models
from mongodb_connection import db

# Create your models here.

class Author:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone
        self.books = []

    def save(self):
        result = db.authors.insert_one({'name': self.name, 'email': self.email, 'phone': self.phone, 'books': self.books})
        return result.inserted_id

class Publisher:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

    def save(self):
        result = db.publishers.insert_one({'name': self.name, 'email': self.email, 'phone': self.phone})
        return result.inserted_id

class Category:
    def __init__(self, name):
        self.name = name
        self.books = []

    def save(self):
        result = db.categories.insert_one({'name': self.name, 'books': self.books})
        return result.inserted_id

class Book:
    def __init__(self, title, authors, publisher, categories):
        self.title = title
        self.authors = authors
        self.publisher = publisher
        self.categories = categories

    def save(self):
        author_ids = [author for author in self.authors]
        publisher_id = self.publisher
        category_ids = [category for category in self.categories]

        result = db.books.insert_one({
            'title': self.title,
            'authors': author_ids,
            'publisher': publisher_id,
            'categories': category_ids
        })
        return result.inserted_id

