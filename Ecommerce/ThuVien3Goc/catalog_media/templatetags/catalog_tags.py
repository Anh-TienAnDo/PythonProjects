from django import template
from django.http import HttpResponse
from catalog_media.services import *
from django.core.cache import cache

register = template.Library()

@register.inclusion_tag('templatetags/catalog_box.html')
def catalog_box(request):
    cache_key = 'catalog_box_cache'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return cached_data
    
    categories_service = CategoryService(request=request)
    authors_service = AuthorService(request=request)
    producers_service = ProducerService(request=request)
    
    categories = categories_service.get_list_category()
    authors = authors_service.get_list_author()
    producers = producers_service.get_list_producer()
    
    data = {
        'categories': categories,
        'authors': authors,
        'producer': producers
    }
    
    cache.set(cache_key, data, timeout=60*3)
    
    return data

