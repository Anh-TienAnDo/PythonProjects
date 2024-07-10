from rest_framework import serializers
from .models import USB

class USBSerializer(serializers.ModelSerializer):
    class Meta:
        model = USB
        fields = ['id', 'name', 'slug', 'view', 'producer', 'type', 'image', 'price_old', 'price_new', 'memory', 'description']