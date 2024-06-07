from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from product.models import *
from mobile.models import *
from clothes.models import *
from .cart import _generate_cart_id, CartService
from django.contrib.auth.models import User
from django.conf import settings
from clothes.clothes import *

cartService = None
# Create your views here.
def allCart(req):
    global cartService
    cartService = CartService(request=req)
    result = []
    total = 0
    quantity_item = 0
    if req.user.is_authenticated:
        user = req.user
        for product_slug, item in cartService.cart.items():
            if Cart.objects.filter(user=user, product_slug=product_slug).exists():
                cart_item = Cart.objects.get(user=user, product_slug=product_slug)
                cart_item.quantity += item['quantity']
                cart_item.save()
            else:
                Cart.objects.create(cart_id=_generate_cart_id(), user=user, product_slug=product_slug, quantity=item['quantity'])

        cartService.clear()
        items = Cart.objects.filter(user=user)
        for item in items:
            total += item.getTotal
            product = Product.objects.filter(slug=item.product_slug).first()
            if product is None:
                product = Phone.objects.filter(slug=item.product_slug).first()
            if product is None:
                product = getDetailsClothesServiceUrl(slug=item.product_slug)

            tmp = {}
            tmp['item'] = item
            tmp['product'] = product
            result.append(tmp)
        quantity_item = len(items)

    else:
        total = cartService.get_total_price()
        quantity_item = cartService.__len__
        for product_slug, item in cartService.cart.items():
            product = Product.objects.filter(slug=product_slug).first()
            if product is None:
                product = Phone.objects.filter(slug=product_slug).first()
            if product is None:
                product = getDetailsClothesServiceUrl(slug=product_slug)
            tmp = {}
            tmp['item'] = {
                'quantity': item['quantity'],
                'getTotal': cartService.get_total_price_item(product_slug),
                'product_slug': product_slug,
            }
            tmp['product'] = product
            result.append(tmp)

    content = {
        'page_title': 'cart',
        'result': result,
        'total': total,
        'quantity_item': quantity_item,
    }
    return render(req, 'cart/cart.html', content)

def add(req, slug):
    global cartService
    cartService = CartService(request=req)
    if req.user.is_authenticated:
        user = req.user
        products = Product.objects.all()
        content = {
            'products': products
        }
        cart = Cart.objects.filter(user=user, product_slug=slug)

        if len(cart) == 0:
            Cart.objects.create(cart_id=_generate_cart_id(), user=user, product_slug=slug, quantity=1)
    else:
        product = Product.objects.get(slug=slug)
        cartService.add(product)
    return redirect("/products/")

def addMobile(req, slug):
    global cartService
    cartService = CartService(request=req)
    if req.user.is_authenticated:
        user = req.user
        products = Phone.objects.all()
        content = {
            'products': products
        }
        cart = Cart.objects.filter(user=user, product_slug=slug)

        if len(cart) == 0:
            Cart.objects.create(cart_id=_generate_cart_id(), user=user, product_slug=slug, quantity=1)
    else:
        product = Phone.objects.get(slug=slug)
        cartService.add(product)
    return redirect("/mobiles/")

def addClothes(req, slug):
    global cartService
    cartService = CartService(request=req)
    if req.user.is_authenticated:
        user = req.user
        product = getDetailsClothesServiceUrl(slug=slug)
        content = {
            'product': product
        }
        cart = Cart.objects.filter(user=user, product_slug=slug)

        if len(cart) == 0:
            Cart.objects.create(cart_id=_generate_cart_id(), user=user, product_slug=slug, quantity=1)
    else:
        product = getDetailsClothesServiceUrl(slug=slug)
        cartService.add(Clothes(product))
    return redirect("/clothes/")

def delete(req, slug):
    global cartService
    cartService = CartService(request=req)
    if req.user.is_authenticated:
        item = Cart.objects.get(product_slug=slug)
        item.delete()
    else:
        product = Product.objects.filter(slug=slug).first()
        if product is None:
            product = Phone.objects.filter(slug=slug).first()
        if product is None:
            product = Clothes(getDetailsClothesServiceUrl(slug=slug))
        cartService.remove(product)
    return redirect("/carts/")

def update(req):
    up = req.GET.get('up')
    down = req.GET.get('down')
    global cartService
    cartService = CartService(request=req)
    if req.user.is_authenticated:
        if up:
            cart = Cart.objects.get(product_slug=str(up))
            cart.quantity = cart.quantity + 1
            cart.save()
        elif down:
            cart = Cart.objects.get(product_slug=str(down))
            cart.quantity = cart.quantity - 1
            if cart.quantity <= 0:
                cart.delete()
            else:
                cart.save()
    else:
        if up:
            slug = str(up)
            product = Product.objects.filter(slug=slug).first()
            if product is None:
                product = Phone.objects.filter(slug=slug).first()
            if product is None:
                product = Clothes(getDetailsClothesServiceUrl(slug=slug))
            cartService.add(product, update="up")
        if down:
            slug = str(down)
            product = Product.objects.filter(slug=slug).first()
            if product is None:
                product = Phone.objects.filter(slug=slug).first()
            if product is None:
                product = Clothes(getDetailsClothesServiceUrl(slug=slug))
            cartService.add(product, update="down")

    return redirect('/carts/')
