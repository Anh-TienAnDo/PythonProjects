from django.urls import path
from .views import MemoryStickSearchAndFilterView, MemoryStickFilterView, MemoryStickView, MemoryStickDetailView

urlpatterns = [
    # GET /api/.../?_start=0&_limit=12
    path('', MemoryStickView.as_view()),
    path('detail/<slug:slug>/', MemoryStickDetailView.as_view()),
    path('search-and-filter/', MemoryStickSearchAndFilterView.as_view()),
    path('filter/', MemoryStickFilterView.as_view()),
]