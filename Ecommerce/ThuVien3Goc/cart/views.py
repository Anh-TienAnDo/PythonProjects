import logging
from django.shortcuts import render, redirect
from .service import CartServiceLogged, CartServiceNotLogged
from django.http import JsonResponse
from django.views.generic import View

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create your views here.

def get_all_item(request):
    logger.info('get_all_item called')
    logger.info(f"Session account: {request.session.get('account')}")
    cart_items = []
    if 'account' in request.session:
        cart = CartServiceLogged(request)
        cart_items = cart.get_cart_items()
    else:
        cart = CartServiceNotLogged(request)
        cart_items = cart.get_cart_items()
        
    total_price = cart.get_total_price()
    total_quantity = cart.get_total_quantity()
    
    content = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity,
        'page_title': 'Giỏ hàng',
    }
    # return JsonResponse(content)
    return render(request, 'cart/index.html', content)

def add_item(request, product_slug, product_type):
    logger.info('add_item called')
    logger.info(f"Product slug: {product_slug}, Product type: {product_type}")
    if 'account' in request.session:
        cart = CartServiceLogged(request)
        cart.add(product_slug=product_slug, product_type=product_type)
    else:
        cart = CartServiceNotLogged(request)
        cart.add(product_slug=product_slug, product_type=product_type)
    
    if 'HTTP_REFERER' in request.META:
        return redirect(request.META['HTTP_REFERER'])
    return redirect('core:index')

def remove_item(request, product_slug):
    logger.info('remove_item called')
    logger.info(f"Product slug: {product_slug}")
    if 'account' in request.session:
        cart = CartServiceLogged(request)
        cart.remove(product_slug=product_slug)
    else:
        cart = CartServiceNotLogged(request)
        cart.remove(product_slug=product_slug)
    
    return redirect('cart:index')

def update_item(request, product_slug, action):
    logger.info('update_item called')
    logger.info(f"Product slug: {product_slug}, Action: {action}")
    if 'account' in request.session:
        cart = CartServiceLogged(request)
        cart.update(product_slug=product_slug, action=action)
    else:
        cart = CartServiceNotLogged(request)
        cart.update(product_slug=product_slug, action=action)
    
    return redirect('cart:index')



