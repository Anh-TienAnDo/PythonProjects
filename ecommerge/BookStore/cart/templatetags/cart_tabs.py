from django import template
from ..models import *
from ..cart import _generate_cart_id, CartService
# from django.contrib.flatpages.models import FlatPage

register = template.Library()

@register.inclusion_tag("tabs/cart-box.html")
def cart_box(request):
    cart_item_count = 0
    if request.user.is_authenticated:
        user = request.user
        cart_item_count = len(Cart.objects.filter(user=user))
    else:
        cartService = CartService(request=request)
        cart_item_count = cartService.__len__
    return {'cart_item_count': cart_item_count}