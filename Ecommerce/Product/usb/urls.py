from django.urls import path
from .views import *

urlpatterns = [
    # GET /api/.../?_start=0&_limit=12
    path('', USBView.as_view()),
    path('<slug:slug>/', USBDetailView.as_view()),
]