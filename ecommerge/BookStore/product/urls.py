from django.urls import path
from . import views

urlpatterns = [
    path('', views.allProduct, name='products'),
    path('details/<slug:slug>', views.detailsProduct, name='product'),
]