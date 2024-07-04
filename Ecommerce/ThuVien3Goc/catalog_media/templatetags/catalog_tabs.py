from django import template
from django.http import HttpResponse
from catalog_media.service import ServiceCategory, ServiceAuthor

register = template.Library()

@register.inclusion_tag('templatetags/catalog_box.html')
def catalog_box(request):
    categories = ServiceCategory().get_list_categories()
    authors = ServiceAuthor().get_list_authors()
    return {'categories': categories, 'authors': authors}

