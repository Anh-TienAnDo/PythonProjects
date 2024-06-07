from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', ClothesListCreateView.as_view(), name='clothes-list-create'),
    path('<int:id>/', ClothesRetrieveUpdateDestroyAPIViewID.as_view(), name='clothes-detail-id'),
    path('slug/<slug:slug>/', ClothesRetrieveUpdateDestroyAPIViewSLUG.as_view(), name='clothes-detail-slug'),
    path('producers/', ProducerListCreateView.as_view(), name='producer-list-create'),
    path('producers/<int:pk>/', ProducerDetailView.as_view(), name='producer-detail'),
    path('types/', TypeListCreateView.as_view(), name='type-list-create'),
    path('types/<int:pk>/', TypeDetailView.as_view(), name='type-detail'),
]