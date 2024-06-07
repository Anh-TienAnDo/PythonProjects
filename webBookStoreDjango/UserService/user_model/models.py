from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser

# Create your models here.
class Address(models.Model):
    street = models.CharField(max_length=255, null=True)
    district = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    note = models.TextField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.street}, {self.district}, {self.city}"

class NameUser(models.Model):
    fullname = models.CharField(max_length=255, null=True)
    fname = models.CharField(max_length=255, null=True)
    lname = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.lname + " " + self.fname)


class Account(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)
    first_name = None
    last_name = None

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

class User(models.Model):
    account = models.OneToOneField(Account, on_delete=models.SET_NULL, null=True)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True)
    name_user = models.OneToOneField(NameUser, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=12, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.account.username


# class Account(models.Model):
#     username = models.CharField(max_length=255, unique=True)
#     password = models.CharField(max_length=255, null=True)
#     email = models.EmailField(max_length=255, null=True)
#     is_staff = models.BooleanField(default=False)
#     is_super = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.username

