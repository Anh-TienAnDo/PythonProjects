from django import template
from django.http import HttpResponse
from catalog_media.services import ServiceAuthor, ServiceCategory, ServiceProducer

register = template.Library()

@register.inclusion_tag('templatetags/audiobook-filter-form.html')
def filter_box(request):
    author_service = ServiceAuthor(request=request)
    category_service = ServiceCategory(request=request)
    producer_service = ServiceProducer(request=request)
    
    authors = author_service.get_list_authors()
    categories = category_service.get_list_categories()
    producers = producer_service.get_list_producers()
    return {
        'authors': authors,
        'categories': categories,
        'producers': producers,
    }

