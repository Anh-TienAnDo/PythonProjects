from django.urls import path
from . import views

urlpatterns = [
    path('authors/', views.get_list_author, name='get_list_author'),
    path('authors/<int:id>/', views.get_detail_author, name='get_detail_author'),
    path('categories/', views.get_list_category, name='get_list_category'),
    path('categories/<int:id>/', views.get_detail_category, name='get_detail_category'),
]