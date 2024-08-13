from django import template
from django.http import HttpResponse
from catalog_media.services import ServiceCategory, ServiceAuthor

register = template.Library()

@register.inclusion_tag('templatetags/catalog_box.html')
def catalog_box(request):
    categories_service = ServiceCategory(request=request)
    authors_service = ServiceAuthor(request=request)
    
    categories = categories_service.get_list_categories()
    authors = authors_service.get_list_authors()
    return {'categories': categories, 'authors': authors}

