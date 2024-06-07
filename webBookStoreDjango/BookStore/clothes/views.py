from django.shortcuts import render
import requests
from json import *
from .clothes import *

# Create your views here.
def getClothes(req):
    clothes = None
    while clothes is None:
        try:
            clothes = req.session['clothes']
        except:
            clothes = getClothesServiceUrl()
    content = {
        'page_title': 'clothes',
        'products': clothes
    }
    return render(req, 'clothes/clothes.html', content)

def detailsClothes(req, slug):
    clothes = None
    while clothes is None:
        clothes = getDetailsClothesServiceUrl(slug=slug)
    content = {
        'page_title': 'details clothes',
        'product': clothes
    }
    return render(req, 'clothes/details_clothes.html', content)
