from django.template import Library
from cart.models import CartItems
from cart.service import CartServiceLogged, CartServiceNotLogged

register = Library()

@register.inclusion_tag('templatetags/cart_box.html')
def cart_box(request):
    cart_quantity = 0
    if 'account' in request.session:
        cart = CartServiceLogged(request)
        cart_quantity = cart.get_total_quantity
    else:
        cart = CartServiceNotLogged(request)
        cart_quantity = cart.get_total_quantity
    return {
        'cart_quantity': cart_quantity
    }