from django.urls import path
from .views import AppointmentsListCreate, AppointmentsDetail

urlpatterns = [
    path('', AppointmentsListCreate.as_view(), name='appointments_list_create'),
    path('<int:pk>/', AppointmentsDetail.as_view(), name='appointments_detail'),
    
]