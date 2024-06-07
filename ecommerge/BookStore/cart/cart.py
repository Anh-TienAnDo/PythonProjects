from .models import *
from product.models import Product
from mobile.models import Phone
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.conf import settings
import random



# Lấy cart id của người dùng hiện tại, tạo mới nếu trống
def _cart_id(request):
    if not request.session.get(settings.CART_SESSION_ID):
        request.session[settings.CART_SESSION_ID] = _generate_cart_id()
    return request.session[settings.CART_SESSION_ID]

# Tạo cart id mới
def _generate_cart_id():
    cart_id = ''
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
    cart_id_length = 50
    for y in range(cart_id_length):
        cart_id += characters[random.randint(0, len(characters) - 1)]
    return cart_id

# Lấy tất cả các sản phẩm trong giỏ hàng của người dùng hiện tại
def get_cart_items(request):
    return Cart.objects.filter(cart_id=_cart_id(request))

class CartService:
    # initialize the cart
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        # save change
        self.session.modified = True

    # Add product to the cart or update its quantity
    def add(self, product, quantity=1, update=""):
        product_slug = str(product.slug)
        if product_slug not in self.cart:
            self.cart[product_slug] = {
                "quantity": 1,
                "product_id": product.id,
                "product_name": product.name,
                "product_price": product.price,
            }
        # add cart
        if update == "down":
            self.cart[product_slug]["quantity"] -= quantity
            if self.cart[product_slug]["quantity"] <= 0:
                self.remove(product)
        # update cart 
        elif update == "up":
            self.cart[product_slug]["quantity"] += quantity
        self.save()

    # Remove a product from the cart
    def remove(self, product):
        product_slug = str(product.slug)
        if product_slug in self.cart:
            del self.cart[product_slug]
            self.save()

    # Count all items in the cart
    def __len__(self):
        return len(self.cart.keys())
    
    def get_total_price_item(self, product_slug):
        return self.cart[product_slug]["quantity"] * self.cart[product_slug]["product_price"]

    def get_total_price(self):
        return sum(item["product_price"] * item["quantity"] for item in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()