from django.urls import path
from . import views

urlpatterns = [
    path('', views.allCategory, name='categories'),
    path('show-book/<id>/', views.showBooksByCategory, name='category_book'),
    path('show-mobile/<id>/', views.showMobilesByCategory, name='category_mobile'),
    path('show-clothes/<id>/', views.showClothesByCategory, name='category_clothes'),
]