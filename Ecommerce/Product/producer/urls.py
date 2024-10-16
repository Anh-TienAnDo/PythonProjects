from django.urls import path
from .views import *

urlpatterns = [
    path('', ProducerView.as_view(), name='producers'),
    # path('type/', ProducerByTypeView.as_view(), name='producers_by_type'),
]