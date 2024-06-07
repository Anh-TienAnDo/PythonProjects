from django.db import models
from order.models import *

# Create your models here.
class Shipment(models.Model):
    checkout = models.OneToOneField(Checkout, on_delete=models.SET_NULL, null=True)
    shipper = models.CharField(max_length=255)
    delivered = models.BooleanField(default=False)
    date_shipment = models.DateTimeField(auto_now_add=True) 
    note = models.TextField()

    def __str__(self) -> str:
        return str(Checkout)
