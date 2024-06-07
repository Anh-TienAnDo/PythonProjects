from django.shortcuts import render
from .models import *

# Create your views here.
def getMobiles(req):
    products = Phone.objects.all()
    content = {
        'page_title': 'mobiles',
        'products': products
    }
    return render(req, 'mobile/mobiles.html', content)

def detailsMobile(req, slug):
    product = Phone.objects.get(slug=slug)
    content = {'product': product,
               'page_title': 'Mobile details'}
    return render(req, 'mobile/details_product.html', content)
