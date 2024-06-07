from .views import *
from django.urls import path

urlpatterns = [
    path('report-product', report_product, name="report-product"),
    path('report-customer', report_customer, name="report-customer"),
]