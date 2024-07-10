from django.urls import path
from .views import *

urlpatterns = [
    # GET /api/.../?_start=0&_limit=12
    path('', MemoryStickView.as_view()),
    path('<slug:slug>/', MemoryStickDetailView.as_view()),
]