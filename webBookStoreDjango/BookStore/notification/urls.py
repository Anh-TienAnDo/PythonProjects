from .views import *
from . import service
from django.urls import path

urlpatterns = [
    # api notification
    path('email', service.send_email),
]