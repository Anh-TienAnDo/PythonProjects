from django.urls import path
from . import views

urlpatterns = [
    path('', views.allCategory, name='categories'),
    path('show/<slug:slug>', views.showProductByCategory, name='category_product'),
]