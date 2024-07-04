from typing import Iterable
from django.db import models
import random

# Create your models here.

class Checkout(models.Model):
    # set of possible order statuses
    ORDER_STATUSES = {
        '1': 'PENDING',
        '2': 'SHIPPED',
        '3': 'DELIVERED',
        '4': 'CANCELLED',
    }
    code = models.CharField(max_length=20, unique=True)
    user_id = models.BigIntegerField(default=1)
    person_name = models.CharField(max_length=255, null=True)
    address = models.TextField()
    phone = models.CharField(max_length=12, null=True)
    email = models.EmailField(max_length=255, null=True)
    total = models.BigIntegerField(default=0)
    status = models.CharField(max_length=1, choices=ORDER_STATUSES, default='1')
    date_order = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.code)
    
    def generate_code(self):
        code = ''
        characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
        code_length = 20
        for y in range(code_length):
            code += characters[random.randint(0, len(characters) - 1)]
        return code
    
    def save(self, *args, **kwargs):
        self.code = self.generate_code()
        super(Checkout, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Checkouts'

class OrderItems(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    product_slug = models.SlugField(null=True)
    price = models.BigIntegerField(default=0)
    quantity = models.IntegerField(default=1, blank=True)
    checkout = models.ForeignKey(Checkout, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.product_slug)
    
    @property
    def total(self):
        return self.quantity * self.price
    
    class Meta:
        verbose_name_plural = 'OrderItems'


