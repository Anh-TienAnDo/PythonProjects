from django.db import models
from product.models import *
from mobile.models import *
from clothes.models import *
from clothes.clothes import *
from django.contrib.auth.models import User
# from order.models import Order

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product_slug = models.SlugField(null=True)
    quantity = models.IntegerField(default=1, blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'cart'

    def __str__(self):
        return str(self.id)

    @property
    def get_all_item(self):
        items = Cart.objects.all()
        return len(items)

    @property
    def getTotal(self):
        product = Product.objects.filter(slug=self.product_slug).first()
        if product is None:
            product = Phone.objects.filter(slug=self.product_slug).first()
        if product is None:
            product = Clothes(getDetailsClothesServiceUrl(slug=self.product_slug))
        return self.quantity * product.price



