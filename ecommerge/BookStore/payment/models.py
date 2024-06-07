from django.db import models
from order.models import *
from django.contrib.auth.models import User

# Create your models here.
class Payment(models.Model):
    user = models.BigIntegerField(null=True)
    checkout = models.OneToOneField(Checkout, on_delete=models.SET_NULL, null=True)
    total = models.BigIntegerField(null=True)
    paymented = models.BigIntegerField(null=True)
    missing = models.BigIntegerField(null=True)
    completed = models.BooleanField(default=False)
    note = models.TextField()
    date_completed = models.DateTimeField(null=True)

