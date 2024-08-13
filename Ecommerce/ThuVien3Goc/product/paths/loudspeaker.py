from django.urls import path
from product.controllers.loudspeaker import *

app_name = 'product-loudspeaker'

urlpatterns = [
    path('', LoudSpeakerView.as_view(), name='loudspeakers'),
    path('search/', LoudSpeakerSearchView.as_view(), name='search'),
    path('detail/<slug:slug>/', LoudSpeakerDetailView.as_view(), name='detail'),
]