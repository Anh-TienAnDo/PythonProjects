from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', BookListCreateView.as_view(), name='book-list-create'),
    path('<int:id>/', BookRetrieveUpdateDestroyAPIViewID.as_view(), name='book-detail-id'),
    path('slug/<slug:slug>/', BookRetrieveUpdateDestroyAPIViewSLUG.as_view(), name='book-detail-slug'),
    path('categories/', CategoryListCreateView.as_view(), name='book-category-list-create'),
    path('categories/<int:id>/', CategoryRetrieveUpdateDestroyAPIViewID.as_view(), name='book-category-detail'),
    path('categories/slug/<slug:slug>/', CategoryRetrieveUpdateDestroyAPIViewSLUG.as_view(), name='book-category-detail-slug'),
    path('books-by-category/<int:id>/', ShowAllBookByCategory.as_view(), name='show-books-by-category'),
    path('search/', BookSearchAPIView.as_view(), name='book-search'),
]