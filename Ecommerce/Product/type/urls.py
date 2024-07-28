from django.urls import path
from .views import *

urlpatterns = [
    path('types/', TypeView.as_view(), name='type'),
]