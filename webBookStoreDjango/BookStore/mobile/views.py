from django.shortcuts import render
import requests
from json import *
from .mobile import *

# Create your views here.
def getMobiles(req):
    mobiles = None
    while mobiles is None:
        try:
            mobiles = req.session['mobiles']
        except:
            mobiles = getMobilesServiceUrl()
    content = {
        'page_title': 'mobiles',
        'products': mobiles
    }
    return render(req, 'mobile/mobiles.html', content)

def detailsMobile(req, slug):
    mobile = None
    while mobile is None:
        mobile = getDetailsMobileServiceUrl(slug=slug)
    content = {'product': mobile,
               'page_title': 'Mobile details'}
    return render(req, 'mobile/details_product.html', content)
