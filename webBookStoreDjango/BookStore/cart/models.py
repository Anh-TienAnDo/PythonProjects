from django.db import models
from django.contrib.auth.models import User
from clothes.clothes import *
from mobile.mobile import *
from book.book import *
from book.models import *
from mobile.models import *
from clothes.models import *
# from order.models import Order

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=50, null=True)
    user_id = models.BigIntegerField(null=True, blank=True)
    product_slug = models.SlugField(null=True)
    quantity = models.IntegerField(default=1, blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'cart'

    def __str__(self):
        return str(self.product_slug)

    # @property
    # def get_all_item(self):
    #     items = Cart.objects.all()
    #     return len(items)

    # @property
    # def getTotal(self):
    #     product = getDetailsBookServiceUrl(slug=self.product_slug)
    #     if product is None:
    #         product = getDetailsMobileServiceUrl(slug=self.product_slug)
    #     if product is None:
    #         product = getDetailsClothesServiceUrl(slug=self.product_slug)
    #     return self.quantity * product['price']



