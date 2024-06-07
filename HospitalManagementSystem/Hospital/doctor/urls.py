from .views import *
from django.urls import path, include

app_name = 'doctor'
urlpatterns = [
    path('', index, name="doctors"),
    path('details/<int:id>', doctor_details, name="details"),
    path('<int:id>/delete', delete, name="delete"),
]