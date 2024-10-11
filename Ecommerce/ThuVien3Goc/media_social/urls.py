from django.urls import path, include
from .views import *

urlpatterns = [
    # path('sayings/', include('media_social.paths.sayings')),
    # path('audio-books/', include('media_social.paths.audio_book')),
    # http://127.0.0.1:9999/api/media-socials/filter?_type=sayings
    path('all/<str:_type>', get_all_by_type, name='media-socials'),
    # http://127.0.0.1:9999/api/media-socials/details/sayings/{slug}
    path('details/<str:_type>/<slug:slug>', get_detail, name='media-social'),
    # http://127.0.0.1:9999/api/media-socials/search-filter?_query=a
    path('search', search_and_filter, name='search-media-social'),
]