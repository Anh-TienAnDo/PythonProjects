from django.urls import path
from .views import *

urlpatterns = [
    path('', TypeView.as_view(), name='types'),
    path('get/<slug:slug>/', TypeView.as_view(), name='type_by_slug'),
    path('create/', TypeView.as_view(), name='create_type'),
    path('update/<int:pk>/', TypeView.as_view(), name='update_type'),
    path('delete/<int:pk>/', TypeView.as_view(), name='delete_type'),
]