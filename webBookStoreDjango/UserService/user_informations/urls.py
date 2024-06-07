from . import views
from django.urls import path

urlpatterns = [
    path('user/informations/<int:id>', views.informations, name="informations"),
    path('user/change-password/<int:id>', views.change_password, name="change-password"),
]