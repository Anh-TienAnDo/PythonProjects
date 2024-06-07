from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .cart import _generate_cart_id, CartService
from django.contrib.auth.models import User
from django.conf import settings
from clothes.clothes import *
from mobile.mobile import *
from book.book import *
import requests, json

cartService = None
# Create your views here.
def get_cart_service(url = 'http://127.0.0.1:9995/carts/api/cart/', user_id=0, product_slug=''):
    url = url + str(user_id) + '/' + str(product_slug)
    response = requests.get(url).json()
    return response

def update_cart_service(url = 'http://127.0.0.1:9995/carts/api/cart/', user_id=0, product_slug='', data={}):
    url = url + str(user_id) + '/' + str(product_slug)
    response = requests.post(url, json=data).json()
    return response

def delete_cart_service(url = 'http://127.0.0.1:9995/carts/api/', user_id=0, product_slug=''):
    url = url + str(user_id) + '/' + str(product_slug) + '/delete'
    response = requests.get(url).json()
    return response

def get_all_cart_service(url = 'http://127.0.0.1:9995/carts/api/', user_id=0):
    print("-----------------------------")
    print("Cart Service: get_all_cart_service -  " + "http://127.0.0.1:9995/carts/api/" + str(user_id))
    url = url + str(user_id) + '/create'
    try:
        response = requests.get(url, timeout=(5, 15))
        response = response.json()
        print("Cart Service Data:")
        print(response.get('data'))
    except requests.exceptions.Timeout:
        print("Timed out")
        response = {'status': 'Failed', 'message': 'Timed out'}
    return response

def create_cart_service(url = 'http://127.0.0.1:9995/carts/api/', user_id=0, data={}):
    url = url + str(user_id) + '/create'
    response = requests.post(url, json=data).json()
    return response

def allCart(req):
    global cartService
    cartService = CartService(request=req)
    result = []
    total = 0
    quantity_item = 0
    if 'user' in req.session:
        user_id = req.session['user'].get('id')
        # items = Cart.objects.filter(user_id=user_id, status=False)
        result_api = get_all_cart_service(user_id=user_id)
        if result_api.get('status') == "Success":
            items = result_api.get('data')
            for item in items:
                product = getDetailsBookServiceUrl(slug=item.get('product_slug'))
                if product is None:
                    product = getDetailsMobileServiceUrl(slug=item.get('product_slug'))
                if product is None:
                    product = getDetailsClothesServiceUrl(slug=item.get('product_slug'))

                tmp = {}
                tmp['item'] = item
                tmp['price'] = int(item.get('quantity')) * int(product.get('price'))
                total += tmp['price']
                tmp['product'] = product
                result.append(tmp)
            quantity_item = len(items)
            req.session['total'] = total
        elif result_api.get('status') == "Failed":
            return HttpResponse(result)

    else:
        total = cartService.get_total_price()
        quantity_item = cartService.__len__
        for product_slug, item in cartService.cart.items():
            product = getDetailsBookServiceUrl(slug=product_slug)
            if product is None:
                product = getDetailsMobileServiceUrl(slug=product_slug)
            if product is None:
                product = getDetailsClothesServiceUrl(slug=product_slug)
            tmp = {}
            tmp['item'] = {
                'quantity': item['quantity'],
                'product_slug': product_slug,
            }
            tmp['price'] = cartService.get_total_price_item(product_slug)
            tmp['product'] = product
            result.append(tmp)

    content = {
        'page_title': 'cart',
        'result': result,
        'total': total,
        'quantity_item': quantity_item,
    }
    print(result)
    return render(req, 'cart/cart.html', content)

def add(req, slug):
    global cartService
    cartService = CartService(request=req)
    if req.method == "GET":
        quantity = 1
    if req.method == "POST":
        quantity = req.POST.get('quantity')
        quantity = int(quantity)
        
    if 'user' in req.session:
        user_id = req.session['user'].get('id')
        result = create_cart_service(user_id=user_id, data={'user_id': user_id,
                                                            'product_slug': slug,
                                                            'quantity': quantity,})
        if result.get('status') == "Failed":
            return HttpResponse(result)
        
        # cart = Cart.objects.filter(user_id=user_id, product_slug=slug)

        # if len(cart) == 0:
        #     Cart.objects.create(cart_id=_generate_cart_id(), user_id=user_id, product_slug=slug, quantity=quantity)
        # else:
        #     cart = cart.first()
        #     cart.quantity = cart.quantity + quantity
        #     cart.save()
    else:
        product = getDetailsBookServiceUrl(slug=slug)
        cartService.add(product, quantity=quantity)
    
    if 'HTTP_REFERER' in req.META:
        return redirect(req.META['HTTP_REFERER'])
    return redirect("/books/")

def addMobile(req, slug):
    global cartService
    cartService = CartService(request=req)
    if req.method == "GET":
        quantity = 1
    if req.method == "POST":
        quantity = req.POST.get('quantity')
        quantity = int(quantity)
        
    if 'user' in req.session:
        user_id = req.session['user'].get('id')
        result = create_cart_service(user_id=user_id, data={'user_id': user_id,
                                                            'product_slug': slug,
                                                            'quantity': quantity,})
        if result.get('status') == "Failed":
            return HttpResponse(result)
        # cart = Cart.objects.filter(user_id=user_id, product_slug=slug)

        # if len(cart) == 0:
        #     Cart.objects.create(cart_id=_generate_cart_id(), user_id=user_id, product_slug=slug, quantity=quantity)
        # else:
        #     cart = cart.first()
        #     cart.quantity = cart.quantity + quantity
        #     cart.save()
    else:
        product = getDetailsMobileServiceUrl(slug=slug)
        cartService.add(product, quantity=quantity)
    
    if 'HTTP_REFERER' in req.META:
        return redirect(req.META['HTTP_REFERER'])
    return redirect("/mobiles/")

def addClothes(req, slug):
    global cartService
    cartService = CartService(request=req)
    if req.method == "GET":
        quantity = 1
    if req.method == "POST":
        quantity = req.POST.get('quantity')
        quantity = int(quantity)
    if 'user' in req.session:
        user_id = req.session['user'].get('id')
        result = create_cart_service(user_id=user_id, data={'user_id': user_id,
                                                            'product_slug': slug,
                                                            'quantity': quantity,})
        if result.get('status') == "Failed":
            return HttpResponse(result)
        # cart = Cart.objects.filter(user_id=user_id, product_slug=slug)

        # if len(cart) == 0:
        #     Cart.objects.create(cart_id=_generate_cart_id(), user_id=user_id, product_slug=slug, quantity=quantity)
        # else:
        #     cart = cart.first()
        #     cart.quantity = cart.quantity + quantity
        #     cart.save()
    else:
        product = getDetailsClothesServiceUrl(slug=slug)
        cartService.add(product, quantity=quantity)

    if 'HTTP_REFERER' in req.META:
        return redirect(req.META['HTTP_REFERER'])
    return redirect("/clothes/")

def delete(req, slug):
    global cartService
    cartService = CartService(request=req)
    if 'user' in req.session:
        user_id = req.session['user'].get('id')
        result = delete_cart_service(user_id=user_id, product_slug=slug)
        if result.get('status') == "Failed":
            return HttpResponse(result)
        # item = Cart.objects.get(user_id=user_id, product_slug=slug)
        # item.delete()
    else:
        product = getDetailsBookServiceUrl(slug=slug)
        if product is None:
            product = getDetailsMobileServiceUrl(slug=slug)
        if product is None:
            product = getDetailsClothesServiceUrl(slug=slug)
        cartService.remove(product)
    return redirect("/carts/")

def update(req):
    up = req.GET.get('up')
    down = req.GET.get('down')
    slug = ""
    global cartService
    cartService = CartService(request=req)
    if 'user' in req.session:
        user_id = req.session['user'].get('id')
        if up:
            quantity = 1
            slug = str(up)
            # cart = Cart.objects.get(user_id=user_id, product_slug=str(up), status=False)
            # cart.quantity = cart.quantity + 1
            # cart.save()
        elif down:
            quantity = -1
            slug = str(down)
        result = update_cart_service(user_id=user_id, product_slug=slug, data = {'quantity': quantity})
        if result.get('status') == "Failed":
            return HttpResponse(result)
            # cart = Cart.objects.get(user_id=user_id, product_slug=str(down), status=False)
            # cart.quantity = cart.quantity - 1
            # if cart.quantity <= 0:
            #     cart.delete()
            # else:
            #     cart.save()
    else:
        if up:
            slug = str(up)
            product = getDetailsBookServiceUrl(slug=slug)
            if product is None:
                product = getDetailsMobileServiceUrl(slug=slug)
            if product is None:
                product = getDetailsClothesServiceUrl(slug=slug)
            cartService.update(product, update="up")
        elif down:
            slug = str(down)
            product = getDetailsBookServiceUrl(slug=slug)
            if product is None:
                product = getDetailsMobileServiceUrl(slug=slug)
            if product is None:
                product = getDetailsClothesServiceUrl(slug=slug)
            cartService.update(product, update="down")

    return redirect('/carts/')
