from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('', views.order_list, name='history'),
    path('<int:order_id>/orderitems/', views.orderitems, name='orderitems'),
    path('<int:order_id>/cancel/', views.cancel_order, name='cancel'),
    path('<int:order_id>/re-cancel/', views.re_cancel_order, name='re-cancel'),
    
]