from django import template
from django.http import HttpResponse
from ..models import *
from ..cart import _generate_cart_id, CartService
from ..views import get_all_cart_service
# from django.contrib.flatpages.models import FlatPage

register = template.Library()

@register.inclusion_tag("tabs/cart-box.html")
def cart_box(request):
    cart_item_count = 0
    if 'user' in request.session:
        user_id = request.session['user'].get('id')
        result = get_all_cart_service(user_id=user_id)
        if result.get('status') == "Failed":
            return HttpResponse(result)
        cart_item_count = len(result.get('data'))
        # cart_item_count = len(Cart.objects.filter(user_id=user_id, status=False))
        
    else:
        cartService = CartService(request=request)
        cart_item_count = cartService.__len__
    return {'cart_item_count': cart_item_count}