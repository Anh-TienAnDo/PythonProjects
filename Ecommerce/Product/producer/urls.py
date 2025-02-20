from django.urls import path
from .views import *

urlpatterns = [
    path('', ProducerView.as_view(), name='producers'),
    path('get/<slug:slug>/', ProducerView.as_view(), name='producer_by_slug'),
    path('create/', ProducerView.as_view(), name='create_producer'),
    path('update/<int:pk>/', ProducerView.as_view(), name='update_producer'),
    path('delete/<int:pk>/', ProducerView.as_view(), name='delete_producer'),
]