from django.db import models
from django.contrib.auth.models import User

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
