from .views import *
from django.urls import path, include

app_name = 'patientln'
urlpatterns = [
    path('', patients, name='patients'),
    path('<int:pk>', patient_details, name='patient_details'),
    path('create/', patient_create, name='patient_create'),
    path('<int:pk>/delete/', patient_delete, name='patient_delete'),
    path('<int:pk>/history_medical_list/', patient_history_medical_list, name='history_medical_list'),
    path('history_medical/<int:pk>/', patient_history_medical_details, name='history_medical_details'),
    path('<int:pk>/history_medical/create/', patient_history_medical_create, name='history_medical_create'),
    path('history_medical/<int:pk>/delete/', patient_history_medical_delete, name='history_medical_delete'),
    path('history_medical/<int:pk>/doctor/', patient_history_medical_doctor, name='history_medical_doctor'),
]