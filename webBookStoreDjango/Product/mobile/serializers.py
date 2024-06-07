from rest_framework import serializers
from .models import *

class MobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = "__all__"
        
class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"

class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = "__all__"
