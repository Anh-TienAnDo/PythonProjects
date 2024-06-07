from .views import *
from django.urls import path

urlpatterns = [
    path('', home, name="home"),
    path('user/register', register, name="register"),
    path('user/login', login_user, name="login-user"),
    path('user/logout', logout_user, name="logout-user"),
    path('user/informations', informations, name="informations-user"),
    path('user/update', update_user, name="update-user"),
    path('user/change-password', update_password, name="change-password"),
]