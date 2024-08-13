from django.urls import path
from media_social.controllers.sayings import *

app_name = 'media_social-sayings'

urlpatterns = [
    path('', SayingsView.as_view(), name='sayings'),
    path('search/', SayingsSearchView.as_view(), name='search'),
    path('detail/<slug:slug>/', SayingsDetailView.as_view(), name='detail'),
]