from django.db import models
from django.contrib.auth.models import User
import random

# Create your models here.
class Checkout(models.Model):
    # each individual status
    SUBMITTED = 1
    PROCESSED = 2
    SHIPPED = 3
    PAYMENTED = 4
    CANCELLED = 5
    # set of possible order statuses
    ORDER_STATUSES = ((SUBMITTED, 'Submitted'),
                      (PROCESSED, 'Processed'),
                      (SHIPPED, 'Shipped'),
                      (PAYMENTED, 'Paymented'),
                      (CANCELLED, 'Cancelled'),)
    
    user_id = models.BigIntegerField(null=True, blank=True)
    code = models.CharField(max_length=10, null=True)
    name = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=12, null=True)
    city = models.CharField(max_length=255, null=True)
    address = models.TextField()
    email = models.EmailField(max_length=50)
    status = models.IntegerField(choices=ORDER_STATUSES, default=SUBMITTED)
    note = models.TextField()
    total = models.BigIntegerField(default=0)
    date_order = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.code

# chọn sản phẩm checkout và bấm nút check out
class OrderItems(models.Model):
    product_slug = models.SlugField(null=True)
    price = models.BigIntegerField(default=0)
    quantity = models.IntegerField(default=1, blank=True)
    checkout = models.ForeignKey(Checkout, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.product_slug)
    
    @property
    def total(self):
        return self.quantity * self.price



    # @property
    # def getTotalItems(self):
    #     carts = self.cart_set.all()
    #     total_carts = sum([cart.quantity for cart in carts])
    #     return total_carts

    # @property
    # def getTotalPrice(self):
    #     carts = self.cart_set.all()
    #     total_price = sum([cart.getTotal for cart in carts])
    #     return total_price