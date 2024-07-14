from django.urls import path
from .views import *

app_name = 'cart'
urlpatterns = [
    path('', get_all_item, name='index'),
    path('add-item/<str:product_slug>/<str:product_type>', add_item, name='add-item'),
    path('remove-item/<str:product_slug>', remove_item, name='remove-item'),
    path('update-item/<str:product_slug>/<str:action>', update_item, name='update-item'),
]