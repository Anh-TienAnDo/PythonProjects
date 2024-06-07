from .views import *
from . import service
from django.urls import path

urlpatterns = [
    path('', getOrders, name="orders"),
    path('checkout/', checkout, name="checkout"),
    path('details/<int:id>', detailsOrder, name="details-order"),
    path('cancel-order/<int:id>', cancelOrder, name="cancel-order"),
    path('re-order/<int:id>', re_Order, name="re-order"),

    # api order
    path('api/order/create', service.create_order),
    path('api/checkouts/<int:user_id>', service.get_checkouts_by_user),
    path('api/checkouts', service.get_checkouts),
    path('api/checkouts/<int:id>/cancel', service.cancel_checkout),
    path('api/checkouts/<int:id>/re_order', service.re_order_checkout),
    path('api/order-items/<int:checkout_id>', service.get_order_items),
    path('api/checkout/<int:checkout_id>', service.get_checkout),
    path('api/all-order-items', service.get_all_order_items),

]