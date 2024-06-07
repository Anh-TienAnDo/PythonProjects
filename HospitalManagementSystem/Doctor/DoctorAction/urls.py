from .views import *
from django.urls import path, include


urlpatterns = [
    path('', DoctorViewSet.as_view()),
    path('<int:id>/', DoctorRetrieveUpdateDestroyAPIViewID.as_view()),
    path('create/', DoctorCreate.as_view(), name='create'),
    path('<int:id>/delete/', DoctorDelete.as_view(), name='delete'),
]

