from django.urls import path
from product.controllers.usb import *

app_name = 'product-usb'

urlpatterns = [
    path('', USBView.as_view(), name='usbs'),
    path('search/', USBSearchView.as_view(), name='search'),
    path('<slug:slug>/', USBDetailView.as_view(), name='detail'),
]