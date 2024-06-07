from .views import *
from django.urls import path, include

app_name = 'appointment'
urlpatterns = [
    path('', appointments, name='appointments'),
    path('<int:pk>/', appointment_details, name='appointment_details'),
    path('<int:pk>/delete/', appointment_delete, name='appointment_delete'),
]