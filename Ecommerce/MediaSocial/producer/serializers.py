from rest_framework import serializers
from .models import Producer

class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ['name', 'email', 'slug', 'is_active']