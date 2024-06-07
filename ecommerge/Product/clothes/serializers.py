from rest_framework import serializers
from .models import *

class ClothesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clothes
        fields = ('id', 'name', 'slug', 'producer_id', 'type_id',
                  'price', 'image', 'is_active', 'description',
                   'created_at', 'updated_at', 'imageURL')
        
class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ('id', 'name')

class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ('id', 'name')
