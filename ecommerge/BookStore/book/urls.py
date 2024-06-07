from django.urls import path, register_converter
from . import views


urlpatterns = [
    path('', views.allBook, name='books'),
    path('search-book', views.searchBooks, name='search_books'),
    path('details/<str:book_id>', views.detailsBook, name='book'),
    path('add-book', views.addBook, name='add_book'),
    path('test', views.test, name='test_book'),

    # path('', views.allBook, name='books'),
    # path('details/<int:id>', views.detailsBook, name='book'),
]