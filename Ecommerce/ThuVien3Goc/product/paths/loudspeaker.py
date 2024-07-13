from django.urls import path
from product.controllers.loudspeaker import *

app_name = 'product-loudspeaker'

urlpatterns = [
    path('', LoudSpeakerView.as_view(), name='loudspeakers'),
    path('search/', LoudSpeakerSearchView.as_view(), name='loudspeaker_search'),
    path('<slug:slug>/', LoudSpeakerDetailView.as_view(), name='loudspeaker_detail'),
]