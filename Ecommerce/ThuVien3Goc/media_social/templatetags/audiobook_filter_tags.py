from django import template
from django.http import HttpResponse
from catalog_media.services import ServiceAuthor, ServiceCategory, ServiceProducer
from django.core.cache import cache

register = template.Library()

@register.inclusion_tag('templatetags/audiobook-filter-form.html')
def filter_box(request):
    cache_key = 'audiobook_filter_box_cache'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return cached_data
    
    author_service = ServiceAuthor(request=request)
    category_service = ServiceCategory(request=request)
    producer_service = ServiceProducer(request=request)
    
    authors = author_service.get_list_authors()
    categories = category_service.get_list_categories()
    producers = producer_service.get_list_producers()
    
    data = {
        'authors': authors,
        'categories': categories,
        'producers': producers
    }
    
    cache.set(cache_key, data, timeout=60*3)
    
    return data

