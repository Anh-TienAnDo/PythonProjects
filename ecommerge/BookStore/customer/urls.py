from django.urls import path
from . import views

urlpatterns = [
    path('', views.allCustomer, name='customers'),
    path('details/<int:id>', views.detailsCustomer, name='customer'),
]