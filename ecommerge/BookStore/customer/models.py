from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=False, null=True)
    name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(unique=True, null=True)
    phone = models.CharField(max_length=12, null=True)
    address = models.TextField
    role = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

