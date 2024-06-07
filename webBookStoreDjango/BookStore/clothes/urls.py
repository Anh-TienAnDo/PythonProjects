from .views import *
from django.urls import path, include

urlpatterns = [
    path('', getClothes, name='clothes'),
    path('details/<slug:slug>', detailsClothes, name='details-clothes'),
]