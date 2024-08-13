from django.urls import path
from .views import *

urlpatterns = [
    path('', AudioBookView.as_view(), name='audio_books'),
    path('detail/<slug:slug>/', AudioBookDetailView.as_view(), name='audio_book_detail'),
    path('filter/', AudioBookFilterView.as_view(), name='audio_book_filter'),
]