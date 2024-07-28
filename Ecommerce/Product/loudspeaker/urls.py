from django.urls import path
from .views import *

urlpatterns = [
    # GET /api/.../?_start=0&_limit=12
    path('', LoudspeakerView.as_view()),
    path('detail/<slug:slug>/', LoudspeakerDetailView.as_view(), name='detail'),
    path('search-by-producer/', LoudspeakerSearchByProducerView.as_view(), name='search-by-producer'),
    path('search-by-name/', LoudspeakerSearchByNameView.as_view(), name='search-by-name'),
    path('filter/', LoudspeakerFilterView.as_view(), name='filter'),
]