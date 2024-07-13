from django.db import models
import random

# Create your models here.
class CartItems(models.Model):
    
    id = models.CharField(max_length=50, primary_key=True)
    user_id = models.BigIntegerField(default=1)
    product_slug = models.SlugField(null=True)
    product_type = models.CharField(max_length=20, default='USB')
    price = models.BigIntegerField(default=0)
    quantity = models.IntegerField(default=1)
    status = models.BooleanField(default=False) # False: not ordered, True: ordered
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'CartItems'

    def __str__(self):
        return str(self.product_slug)
    
    def generate_cart_id(self):
        cart_id = ''
        characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
        cart_id_length = 50
        for y in range(cart_id_length):
            cart_id += characters[random.randint(0, len(characters) - 1)]
        return cart_id
    
    def save(self, *args, **kwargs):
        self.id = self.generate_cart_id()
        super(CartItems, self).save(*args, **kwargs)

