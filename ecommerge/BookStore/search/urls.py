from . import views
from django.urls import path

urlpatterns = [
    # path('', views.home, name="home"),
    path('search/result/', views.search, name="search"),
    path('search_book/result/', views.search, name="search-book"),
    path('search_mobile/result/', views.search, name="search-mobile"),
    path('search_clothes/result/', views.search, name="search-clothes"),
]