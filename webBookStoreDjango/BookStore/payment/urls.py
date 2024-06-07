from django.urls import path
from .views import *
from . import service

urlpatterns = [
    path('', paymentBank, name="payment-bank"),
    path('payment-paypal', payment_paypal, name="payment-paypal"),
    path('execute-paypal', execute_paypal, name="execute-paypal"),
    path('cancel-paypal', cancel_paypal, name="cancel-paypal"),
    path('success-paypal', success_paypal, name="success-paypal"),

    
    # api payment
    path('api/create_or_update', service.create_or_update_payment),
    path('api/get/<int:checkout_id>', service.get_payment_by_checkoutid),

]