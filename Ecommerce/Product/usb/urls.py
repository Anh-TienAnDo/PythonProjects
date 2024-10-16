from django.urls import path
from .views import USBSearchAndFilterView, USBFilterView, USBView, USBDetailView

urlpatterns = [
    # GET /api/.../?_start=0&_limit=12
    path('', USBView.as_view()),
    path('detail/<slug:slug>/', USBDetailView.as_view()),
    path('search-and-filter/', USBSearchAndFilterView.as_view()),
    path('filter/', USBFilterView.as_view()),
]