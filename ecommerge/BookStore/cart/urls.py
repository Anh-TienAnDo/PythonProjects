from . import views
from django.urls import path

urlpatterns = [
    path('', views.allCart, name="cart"),
    path('add/<slug:slug>', views.add, name="add-cart"),
    path('add_mobile/<slug:slug>', views.addMobile, name="add-mobile-to-cart"),
    path('add_clothes/<slug:slug>', views.addClothes, name="add-clothes-to-cart"),
    path('delete/<slug:slug>', views.delete, name="delete-cart"),
    path('update', views.update, name='update-cart')
]