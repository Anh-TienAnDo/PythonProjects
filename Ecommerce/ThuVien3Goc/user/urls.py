from .views import *
from django.urls import path

app_name = "user"

urlpatterns = [
    path('account/register/', register, name="register"),
    path('account/log-in/', login_user, name="log-in"),
    path('account/log-in-ordered/', login_user_ordered, name="log-in-ordered"),
    path('account/log-out/', logout, name="log-out"),
    path('informations/', informations, name="informations"),
    path('account/update/', update, name="update"),
    path('account/change-password/', change_password, name="change-password"),
]