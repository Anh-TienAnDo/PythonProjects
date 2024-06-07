from . import views
from django.urls import path

urlpatterns = [
    # api cart
    path('api/cart/<int:user_id>/<slug:product_slug>', views.get_and_update_cart),
    path('api/<int:user_id>/<slug:product_slug>/delete', views.delete_cart),
    path('api/<int:user_id>/create', views.get_carts_and_create_cart),
]