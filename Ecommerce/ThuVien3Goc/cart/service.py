from django.conf import settings
from product.services.loudspeaker import *
from product.services.memory_stick import *
from product.services.usb import *
from abc import ABC, abstractmethod
from .models import CartItems

class CartService(ABC):
    def __init__(self, request):
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
            if product_type == 'Loudspeaker':
                product = LoudspeakerService.get_loudspeaker_by_slug(slug=product_slug)
            elif product_type == 'USB':
                product = USBService.get_usb_by_slug(slug=product_slug)
            elif product_type == 'MemoryStick':
                product = MemoryStickService.get_memory_stick_by_slug(slug=product_slug)
            else:
                product = None
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
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())
    
    def get_total_quantity(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_cart_items(self):
        return self.cart.values()
    
    def get_cart_items_count(self):
        return len(self.cart)
    
    
class CartServiceLogged(CartService):
    
    def __init__(self, request):
        super().__init__(request)
        user = self.session.get('account')
        self.user_id = user.get('id')
        
    def save(self):
        pass
    
    def add(self, product_slug, product_type, quantity=1):
        product_slug = str(product_slug)
        item = CartItems.objects.filter(user=self.user_id, product_slug=product_slug)
        if item.exists():
            item.quantity += quantity
            item.save()
            return 
        else:
            if product_type == 'Loudspeaker':
                product = LoudspeakerService.get_loudspeaker_by_slug(slug=product_slug)
            elif product_type == 'USB':
                product = USBService.get_usb_by_slug(slug=product_slug)
            elif product_type == 'MemoryStick':
                product = MemoryStickService.get_memory_stick_by_slug(slug=product_slug)
            else:
                product = None
            item = CartItems(user=self.user_id, product_slug=product_slug, product_type=product_type, price=int(product.get('price_new')), quantity=quantity)
            item.save()
            return
        
    def remove(self, product_slug):
        item = CartItems.objects.filter(user=self.user_id, product_slug=product_slug)
        if item.exists():
            item.delete()
            return
        else:
            return
        
    def update(self, product_slug, action=None):
        item = CartItems.objects.filter(user=self.user_id, product_slug=product_slug)
        if item.exists():
            if action == 'up':
                item.quantity += 1
            elif action == 'down':
                item.quantity -= 1
                if item.quantity <= 0:
                    item.delete()
            item.save()
            return
        else:
            return
        
    def get_total_price(self):
        return sum(int(item.price) * item.quantity for item in CartItems.objects.filter(user=self.user_id))
    
    def get_total_quantity(self):
        return sum(item.quantity for item in CartItems.objects.filter(user=self.user_id))
    
    def get_cart_items(self) -> list:
        items = CartItems.objects.filter(user=self.user_id)
        result = []
        for item in items:
            product_type = item.product_type
            if product_type == 'Loudspeaker':
                product = LoudspeakerService.get_loudspeaker_by_slug(slug=item.product_slug)
            elif product_type == 'USB':
                product = USBService.get_usb_by_slug(slug=item.product_slug)
            elif product_type == 'MemoryStick':
                product = MemoryStickService.get_memory_stick_by_slug(slug=item.product_slug)
            else:
                product = None
            result.append(
                {
                    'product_type': product_type,
                    'product_slug': item.product_slug,
                    'quantity': item.quantity,
                    'price': item.price,
                    'image': product.get('image'),
                    'name': product.get('name'),
                })
        return result
                
    def get_cart_items_count(self):
        return CartItems.objects.filter(user=self.user_id).count() 
            
        