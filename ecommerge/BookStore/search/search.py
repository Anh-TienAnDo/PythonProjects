from product.models import Product
from mobile.models import *
from clothes.clothes import *

def searchAll(req, key):
    result = {}
    products = []
    products.extend(Product.objects.filter(name__icontains=key))
    products.extend(Product.objects.filter(author__icontains=key))
    result['products'] = set(products)

    mobiles = []
    mobiles.extend(Phone.objects.filter(name__icontains=key))
    mobiles.extend(Phone.objects.filter(producer_id__name__icontains=key))
    result['mobiles'] = set(mobiles)

    clothes = []
    url = 'http://127.0.0.1:9999/clothes/'
    c = None
    while c is None:
        c = getClothesServiceUrl(url)
    for i in c:
        if key in i["name"]:
            clothes.append(i)
    result['clothes'] = clothes

    return result

def searchProduct(req, key):
    products = []
    products.extend(Product.objects.filter(name__icontains=key))
    products.extend(Product.objects.filter(author__icontains=key))
    return set(products)

def searchMobile(req, key):
    mobiles = []
    mobiles.extend(Phone.objects.filter(name__icontains=key))
    mobiles.extend(Phone.objects.filter(producer_id__name__icontains=key))
    return set(mobiles)

def searchClothes(req, key):
    clothes = []
    url = 'http://127.0.0.1:9999/clothes/'
    c = None
    while c is None:
        c = getClothesServiceUrl(url)
    for i in c:
        if key in i["name"]:
            clothes.append(i)
    return clothes

