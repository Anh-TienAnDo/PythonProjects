from .views import *
from django.urls import path

urlpatterns = [
    # api order
    path('api/order/create', create_order),
    path('api/checkouts/<int:user_id>', get_checkouts_by_user),
    path('api/checkouts', get_checkouts),
    path('api/checkouts/<int:id>/cancel', cancel_checkout),
    path('api/checkouts/<int:id>/re_order', re_order_checkout),
    path('api/order-items/<int:checkout_id>', get_order_items),
    path('api/checkout/<int:checkout_id>', get_checkout),
    path('api/all-order-items', get_all_order_items),

]