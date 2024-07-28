from django.urls import path
from .views import *

urlpatterns = [
    path('producers/', ProducerView.as_view(), name='producer'),
]