from django.urls import path
from product.controllers.memory_stick import *

app_name = 'product-memory_stick'

urlpatterns = [
    path('', MemoryStickView.as_view(), name='memory_sticks'),
    path('search/', MemoryStickSearchView.as_view(), name='search'),
    path('<slug:slug>/', MemoryStickDetailView.as_view(), name='detail'),
]