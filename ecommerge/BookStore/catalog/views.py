from django.shortcuts import render
from .models import *
from product.models import *
from mobile.models import *
# tìm book by catalog
# Create your views here.
def allCategory(req):
    categories = Category.objects.all()
    content = {'categories': categories}
    return render(req, 'catalog/categories.html', content)

def showProductByCategory(req, slug):
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(categories__slug=slug)
    content = {'products': products,
               'page_title': 'Books by' + str(category.name) }
    return render(req, 'product/products.html', content)
