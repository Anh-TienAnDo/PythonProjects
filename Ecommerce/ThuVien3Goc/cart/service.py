from django.conf import settings
from product.services.loudspeaker import *
from product.services.memory_stick import *
from product.services.usb import *
from abc import ABC, abstractmethod
from .models import CartItems
from django.core.cache import cache

def get_product(request, product_slug, product_type):
    if product_type == 'Loudspeaker':
        loudspeaker_service = LoudspeakerService(request=request)
        product = loudspeaker_service.get_loudspeaker_by_slug(slug=product_slug)
    elif product_type == 'USB':
        usb_service = USBService(request=request)
        product = usb_service.get_usb_by_slug(slug=product_slug)
    elif product_type == 'MemoryStick':
        memotystick_service = MemoryStickService(request=request)
        product = memotystick_service.get_memory_stick_by_slug(slug=product_slug)
    else:
        product = None
    return product

class CartService(ABC):
    def __init__(self, request):
        self.request = request
        self.session = request.session
        
    @abstractmethod  
    def save(self):
        pass
    
    @abstractmethod   
    def add(self, product_slug, product_type, quantity=1):
        pass
        
    @abstractmethod 
    def remove(self, product_slug):
        pass
        
    @abstractmethod     
    def update(self, product_slug, action=None):
        pass
     
    @abstractmethod    
    def get_total_price(self):
        pass
    
    @abstractmethod 
    def get_total_quantity(self):
        pass
    
    @abstractmethod 
    def get_cart_items(self):
        pass
    
    @abstractmethod
    def get_cart_items_count(self):
        pass               
    
class CartServiceNotLogged(CartService):
    def __init__(self, request):
        super().__init__(request)
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
        
    def add(self, product_slug, product_type, quantity=1):
        product_slug = str(product_slug)
        if product_slug not in self.cart:
            product = get_product(self.request, product_slug, product_type)
            self.cart[product_slug] = {'product_type': product_type, 'quantity': 0, 'price': int(product.get('price_new')), 'image': product.get('image'), 'name': product.get('name')}
        self.cart[product_slug]['quantity'] += quantity
        self.save()
        
    def remove(self, product_slug):
        product_slug = str(product_slug)
        if product_slug in self.cart:
            del self.cart[product_slug]
            self.save()
            
    def update(self, product_slug, action=None):
        product_slug = str(product_slug)
        if action == 'up':
            self.cart[product_slug]['quantity'] += 1
        elif action == 'down':
            self.cart[product_slug]['quantity'] -= 1
            if self.cart[product_slug]['quantity'] <= 0:
                self.remove(product_slug)
        self.save()
        
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
        
    def get_total_price(self):
        total_price = sum(int(item['price']) * item['quantity'] for item in self.cart.values())
        return total_price
    
    def get_total_quantity(self):
        total_quantity = sum(item['quantity'] for item in self.cart.values())
        return total_quantity
    
    def get_cart_items(self) -> list:
        cart_items = []
        for key, item in self.cart.items():
            price_of_item = int(item.get('price')) * int(item.get('quantity'))
            cart_items.append({
                'product_slug': key,
                'product_type': item.get('product_type'),
                'quantity': item.get('quantity'),
                'price': item.get('price'),
                'price_of_item': price_of_item,
                'name': item.get('name'),
                'image': item.get('image'),
            })
        return cart_items
    
    def get_cart_items_count(self):
        count = len(self.cart)
        return count
       
class CartServiceLogged(CartService):
    
    def __init__(self, request):
        super().__init__(request)
        user = self.session.get('account')
        self.user_id = user.get('id')
        
    def save(self):
        pass
    
    def add(self, product_slug, product_type, quantity=1):
        product_slug = str(product_slug)
        item = CartItems.objects.filter(user_id=self.user_id, product_slug=product_slug).first()
        if item:
            item.quantity += quantity
            item.save()
        else:
            product = get_product(self.request, product_slug, product_type)
            item = CartItems(user_id=self.user_id, product_slug=product_slug, product_type=product_type, price=int(product.get('price_new')), quantity=quantity)
            item.save()
        
    def remove(self, product_slug):
        item = CartItems.objects.filter(user_id=self.user_id, product_slug=product_slug)
        if item.exists():
            item.delete()
        
    def update(self, product_slug, action=None):
        item = CartItems.objects.filter(user_id=self.user_id, product_slug=product_slug).first()
        if item:
            if action == 'up':
                item.quantity += 1
                item.save()
            elif action == 'down':
                item.quantity -= 1
                if item.quantity <= 0:
                    item.delete()
                else:
                    item.save()
        
    def get_total_price(self):
        total_price = sum(int(item.price) * item.quantity for item in CartItems.objects.filter(user_id=self.user_id))
        return total_price
    
    def get_total_quantity(self):
        total_quantity = sum(item.quantity for item in CartItems.objects.filter(user_id=self.user_id))
        return total_quantity
    
    def get_cart_items(self) -> list:
        items = CartItems.objects.filter(user_id=self.user_id)
        result = []
        for item in items:
            product_type = item.product_type
            product_slug = item.product_slug
            product = get_product(self.request, product_slug, product_type)
            result.append(
                {
                    'product_type': product_type,
                    'product_slug': item.product_slug,
                    'quantity': item.quantity,
                    'price': item.price,
                    'image': product.get('image'),
                    'name': product.get('name'),
                    'price_of_item': int(item.price) * item.quantity,
                })
        return result
                
    def get_cart_items_count(self):
        count = CartItems.objects.filter(user_id=self.user_id).count()
        return count
    
    def get_cart_in_session_on_db(self):
        items_in_session = self.session.get(settings.CART_SESSION_ID)
        if not items_in_session:
            return
        for product_slug, item in items_in_session.items():
            cart_item = CartItems.objects.filter(user_id=self.user_id, product_slug=product_slug).first()
            if cart_item:
                cart_item.quantity += item['quantity']
                cart_item.save()
            else:
                cart_item = CartItems(user_id=self.user_id, product_slug=product_slug, product_type=item['product_type'], price=item['price'], quantity=item['quantity'])
                cart_item.save()
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

