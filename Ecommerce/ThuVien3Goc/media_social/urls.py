from django.urls import path
from .views import *

app_name = 'media_social'

urlpatterns = [
    path('sayings/', get_sayings, name='sayings'),
    path('sayings/<slug:slug>/', get_detail_saying, name='detail_saying'),
]