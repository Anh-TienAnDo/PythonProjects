from django.db import models

# Create your models here.
class Shipment(models.Model):
    checkout = models.BigIntegerField(null=True, unique=True)
    code = models.CharField(max_length=15, null=True)
    shipper = models.CharField(max_length=255)
    delivered = models.BooleanField(default=False)
    date_shipment = models.DateTimeField(auto_now_add=True) 
    note = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.code)
    
