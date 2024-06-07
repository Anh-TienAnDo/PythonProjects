from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def allProduct(req):
    products = Product.objects.all()
    content = {'products': products}
    return render(req, 'product/products.html', content)

def detailsProduct(req, slug):
    product = Product.objects.get(slug=slug)
    content = {'product': product}
    return render(req, 'product/details_product.html', content)

































# def allProduct(req):
#     products = Product.objects.all()
#     content = {'products': products}
#     return render(req, 'product/products.html', content)
#
# def detailsProduct(req, id):
#     product = Product.objects.get(id=id)
#     content = {'product': product}
#     return render(req, 'product/details_product.html', content)
