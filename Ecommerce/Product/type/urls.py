from django.urls import path
from .views import *

urlpatterns = [
    path('', TypeView.as_view(), name='types'),
]