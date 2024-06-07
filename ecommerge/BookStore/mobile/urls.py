from django.urls import path
from . import views

urlpatterns = [
    path('', views.getMobiles, name='mobiles'),
    path('details/<slug:slug>', views.detailsMobile, name='mobile'),
]