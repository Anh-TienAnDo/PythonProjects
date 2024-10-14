from django.urls import path, include
from .views import *

# media-social/
app_name = 'media_social'
urlpatterns = [
    # path('sayings/', include('media_social.paths.sayings')),
    # path('audio-books/', include('media_social.paths.audio_book')),

    path('all/<str:type_media>', get_all_by_type, name='media_socials'),
    path('details/<str:type_media>/<slug:slug>', get_detail, name='media_social'),
    path('search', search_and_filter, name='search'),
]