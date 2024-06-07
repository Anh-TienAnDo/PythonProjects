from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', ClothesListCreateView.as_view(), name='clothes-list-create'),
    path('<int:id>/', ClothesRetrieveUpdateDestroyAPIViewID.as_view(), name='clothes-detail-id'),
    path('slug/<slug:slug>/', ClothesRetrieveUpdateDestroyAPIViewSLUG.as_view(), name='clothes-detail-slug'),
    path('producers/', ProducerListCreateView.as_view(), name='clothes-producer-list-create'),
    path('producers/<int:id>/', ProducerRetrieveUpdateDestroyAPIViewID.as_view(), name='clothes-producer-detail'),
    path('producers/slug/<slug:slug>/', ProducerRetrieveUpdateDestroyAPIViewSLUG.as_view(), name='clothes-producer-detail-slug'),
    path('types/', TypeListCreateView.as_view(), name='clothes-type-list-create'),
    path('types/<int:id>/', TypeRetrieveUpdateDestroyAPIViewID.as_view(), name='clothes-type-detail'),
    path('types/slug/<slug:slug>/', TypeRetrieveUpdateDestroyAPIViewSLUG.as_view(), name='clothes-type-detail-slug'),
    path('clothes-by-type/<int:id>/', ShowAllClothesByType.as_view(), name='show-clothes-by-type'),
    path('search/', ClothesSearchAPIView.as_view(), name='clothes-search'),

]