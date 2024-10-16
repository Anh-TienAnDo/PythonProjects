from django import template
from catalog_media.services import *
from django.core.cache import cache

register = template.Library()


@register.inclusion_tag('templatetags/mediasocial-search-and-filter-form.html')
def filter_box(request, query, type_media):
    cache_key = 'mediasocial_filter_box_cache'
    cached_data = cache.get(cache_key)

    if cached_data:
        data = cached_data
        data['query'] = query
        data['type_media'] = type_media
        return data

    categories_service = CategoryService(request=request)
    authors_service = AuthorService(request=request)
    producers_service = ProducerService(request=request)

    categories = categories_service.get_list_category()
    authors = authors_service.get_list_author()
    producers = producers_service.get_list_producer()

    data = {
        'authors': authors,
        'categories': categories,
        'producers': producers
    }
    cache.set(cache_key, data, timeout=60 * 3)
    data['query'] = query
    data['type_media'] = type_media
    return data

