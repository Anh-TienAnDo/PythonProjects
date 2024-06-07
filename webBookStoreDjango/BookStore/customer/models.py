from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Address(models.Model):
    street = models.CharField(max_length=255, null=True)
    district = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    note = models.TextField(null=True)

    def __str__(self):
        return " ".join(self.street, self.district, self.city) 

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=12, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username

