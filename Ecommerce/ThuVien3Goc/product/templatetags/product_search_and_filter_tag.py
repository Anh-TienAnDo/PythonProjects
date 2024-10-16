from django import template
from django.http import HttpResponse
from product.services.product import *
from django.core.cache import cache

register = template.Library()

@register.inclusion_tag('templatetags/product-search-filter-form.html')
def filter_box(request, query):
    cache_key = 'product_filter_box_cache'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        data = cached_data
        data['query'] = query
        return data
    
    producer_service = ProductProducerService()
    type_service = ProductTypeService()
    producers = producer_service.get_all_product_producer()
    types = type_service.get_all_product_type()
    
    data = {
        'producers': producers,
        'types': types
    }
    
    cache.set(cache_key, data, timeout=60*3)
    data['query'] = query
    
    return data

