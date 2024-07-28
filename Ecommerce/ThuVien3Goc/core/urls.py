from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
    path('home/', index, name='home'),
    path('search/', search, name='search'),
]