from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', PhoneListCreateView.as_view(), name='phone-list-create'),
    path('<int:id>/', PhoneRetrieveUpdateDestroyAPIViewID.as_view(), name='phone-detail-id'),
    path('slug/<slug:slug>/', PhoneRetrieveUpdateDestroyAPIViewSLUG.as_view(), name='phone-detail-slug'),
    path('producers/', ProducerListCreateView.as_view(), name='mobile-producer-list-create'),
    path('producers/<int:id>/', ProducerRetrieveUpdateDestroyAPIViewID.as_view(), name='mobile-producer-detail'),
    path('producers/slug/<slug:slug>/', ProducerRetrieveUpdateDestroyAPIViewSLUG.as_view(), name='mobile-producer-detail-slug'),
    path('types/', TypeListCreateView.as_view(), name='mobile-type-list-create'),
    path('types/<int:id>/', TypeRetrieveUpdateDestroyAPIViewID.as_view(), name='mobile-type-detail'),
    path('types/slug/<slug:slug>/', TypeRetrieveUpdateDestroyAPIViewSLUG.as_view(), name='mobile-type-detail-slug'),
    path('mobiles-by-type/<int:id>/', ShowAllMobilesByType.as_view(), name='show-mobiles-by-type'),
    path('search/', MobileSearchAPIView.as_view(), name='mobile-search'),

]