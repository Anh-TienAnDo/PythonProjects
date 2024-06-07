from .views import *
from django.urls import path, include

app_name = 'user'
urlpatterns = [
    path('login', login, name="login"),
    path('logout', logout, name="logout"),
    path('informations', informations, name="informations"),
]