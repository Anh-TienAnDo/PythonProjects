from rest_framework import serializers
from .models import *


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', 'email', 'password', 'is_superuser', 'is_staff', 'is_active', 'date_joined']

class NameUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NameUser
        fields = ['fullname', 'fname', 'lname']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'district', 'city']

class PersonSerializer(serializers.ModelSerializer):
    name_user = NameUserSerializer()
    address = AddressSerializer()
    account = AccountSerializer()
    class Meta:
        model = Person
        fields = "__all__"