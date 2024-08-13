
from django.urls import path, include

urlpatterns = [
    path('sayings/', include('media_social.paths.sayings')),
    path('audio-books/', include('media_social.paths.audio_book')),
]