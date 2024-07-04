from rest_framework import serializers
from .models import Checkout, OrderItems

class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = '__all__'

class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['id', 'product_slug', 'price', 'quantity', 'checkout']