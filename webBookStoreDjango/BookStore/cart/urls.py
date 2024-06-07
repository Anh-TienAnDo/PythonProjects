from . import views, service
from django.urls import path

urlpatterns = [
    path('', views.allCart, name="cart"),
    path('add/<slug:slug>', views.add, name="add-cart"),
    path('add_mobile/<slug:slug>', views.addMobile, name="add-mobile-to-cart"),
    path('add_clothes/<slug:slug>', views.addClothes, name="add-clothes-to-cart"),
    path('delete/<slug:slug>', views.delete, name="delete-cart"),
    path('update', views.update, name='update-cart'),
    # api cart
    path('api/cart/<int:user_id>/<slug:product_slug>', service.get_and_update_cart),
    path('api/<int:user_id>/<slug:product_slug>/delete', service.delete_cart),
    path('api/<int:user_id>/create', service.get_carts_and_create_cart),
]