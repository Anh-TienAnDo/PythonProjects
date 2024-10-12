from django.urls import path
from . import views

# catalog_media/
urlpatterns = [
    path('authors', views.get_list_author, name='get_list_author'),
    path('categories', views.get_list_category, name='get_list_category'),
    path('producers', views.get_list_producer, name='get_list_producer'),
    path('types', views.get_list_type, name='get_list_type'),
]