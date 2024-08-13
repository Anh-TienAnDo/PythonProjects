from django.urls import path
from . import views

urlpatterns = [
    path('authors/', views.get_list_author, name='get_list_author'),
    path('categories/', views.get_list_category, name='get_list_category'),
]