from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Address(models.Model):
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    street = models.CharField(max_length=255, null=True)
    district = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    phone = models.CharField(unique=True, max_length=12, null=True)
    note = models.TextField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.street}, {self.district}, {self.city}"
    
    def get_address(self):
        return f"{self.street}, {self.district}, {self.city}"
    
    class Meta:
        verbose_name_plural = "Addresses"


class Name(models.Model):
    fullname = models.CharField(max_length=255, null=True)
    fname = models.CharField(max_length=255, null=True)
    lname = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.lname + " " + self.fname)
    
    def save(self, *args, **kwargs):
        self.fullname = self.lname + " " + self.fname
        super(Name, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Names"


class Account(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255, default="password")
    first_name = None
    last_name = None

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name_plural = "Accounts"

class User(models.Model):
    account = models.OneToOneField(Account, on_delete=models.SET_NULL, null=True)
    name = models.OneToOneField(Name, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.account.username
    
    class Meta:
        verbose_name_plural = "Users"
