from . import views
from django.urls import path

urlpatterns = [
    path('user/register', views.register, name="register"),
    path('user/login', views.login, name="login"),
]