from django.urls import path
from .views import PatientInformationListCreate, PatientInformationDetail, HistoryMedicalListCreate, HistoryMedicalDetail, HistoryMedicalListByDoctor

urlpatterns = [
    path('information/', PatientInformationListCreate.as_view(), name='patient_information_list_create'),
    path('information/<int:pk>/', PatientInformationDetail.as_view(), name='patient_information_detail'),
    path('<int:pk>/history_medical/', HistoryMedicalListCreate.as_view(), name='history_medical_list_create'),
    path('history_medical/<int:pk>/', HistoryMedicalDetail.as_view(), name='history_medical_detail'),
    path('history_medical/<int:pk>/doctor/', HistoryMedicalListByDoctor.as_view(), name='history_medical_list_doctor'),
]
