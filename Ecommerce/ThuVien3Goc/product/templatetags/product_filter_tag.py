from django import template
from django.http import HttpResponse
from product.services.product import *

register = template.Library()

@register.inclusion_tag('templatetags/product-filter-form.html')
def filter_box(request):
    producer_service = ProdcutProducerService()
    type_service = ProductTypeService()
    producers = producer_service.get_all_product_producer()
    types = type_service.get_all_product_type()
    return {
        'producers': producers,
        'types': types
    }

