from django.urls import path
from .views import *

urlpatterns = [
    # api payment
    path('api/create_or_update', create_or_update_payment),
    path('api/get/<int:checkout_id>', get_payment_by_checkoutid),

]