from django.db import models
from django.contrib.auth.models import User
from cart.models import Cart

# from customer.models import Customer

# Create your models here.

#  điền đầy đủ thông tin và xác nhận
class Checkout(models.Model):
    # each individual status
    SUBMITTED = 1
    PROCESSED = 2
    SHIPPED = 3
    CANCELLED = 4
    # set of possible order statuses
    ORDER_STATUSES = ((SUBMITTED, 'Submitted'),
                      (PROCESSED, 'Processed'),
                      (SHIPPED, 'Shipped'),
                      (CANCELLED, 'Cancelled'),)
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=12, null=True)
    address = models.TextField()
    email = models.EmailField(max_length=50)
    status = models.IntegerField(choices=ORDER_STATUSES, default=SUBMITTED)
    note = models.TextField()
    total = models.BigIntegerField(default=0)
    date_order = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

# chọn sản phẩm checkout và bấm nút check out
class OrderItems(models.Model):
    # cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    product = models.SlugField(null=True)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1, blank=True)
    checkout = models.ForeignKey(Checkout, on_delete=models.SET_NULL, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    # transaction_id = models.CharField(max_length=255, null=True)

    def __str__(self):
        return str(self.product)
    
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