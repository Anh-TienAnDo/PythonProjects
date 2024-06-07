from django.urls import path, register_converter
from .views import *


urlpatterns = [
    path('', getBooks, name='products'),
    path('details/<slug:slug>', detailsBook, name='product'),

]