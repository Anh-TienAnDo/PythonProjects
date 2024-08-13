from django.urls import path
from media_social.controllers.audio_book import *

app_name = 'media_social-audio_book'

urlpatterns = [
    path('', AudioBookView.as_view(), name='audio_books'),
    path('detail/<slug:slug>/', AudioBookDetailView.as_view(), name='detail'),
    
]