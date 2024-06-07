from django.shortcuts import render
from product.models import Product
from mobile.models import *
from .search import *

# Create your views here.
def search(req):
    query = req.GET.get('keyword')
    products = {}
    if query:
        if "/search_book/result/" in req.path:
            products['products'] = searchProduct(req, query)
            products['mobiles'] = None
            products['clothes'] = None
        elif "/search_mobile/result/" in req.path:
            products['mobiles'] = searchMobile(req, query)
            products['products'] = None
            products['clothes'] = None
        elif "/search_clothes/result/" in req.path:
            products['clothes'] = searchClothes(req, query)
            products['products'] = None
            products['mobiles'] = None
        else:
            products = searchAll(req, query)
    else:
        products['products'] = None
        products['mobiles'] = None
        products['clothes'] = None
    context = {
        'page_title': 'result search for product',
        'products': products['products'],
        'mobiles': products['mobiles'],
        'clothes': products['clothes'],
        'query': query,
    }

    return render(req, 'result_search.html', context)

