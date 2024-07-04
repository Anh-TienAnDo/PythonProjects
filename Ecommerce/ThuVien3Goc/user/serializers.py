from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class NameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Name
        fields = ['id', 'fullname', 'fname', 'lname']

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'user', 'street', 'district', 'city', 'phone']