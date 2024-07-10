from rest_framework import serializers
from .models import MemoryStick

class MemoryStickSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryStick
        fields = ['id', 'name', 'slug', 'view', 'producer', 'type', 'image', 'price_old', 'price_new', 'memory', 'description']