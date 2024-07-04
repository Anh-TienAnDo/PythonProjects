from rest_framework import serializers
from .models import Saying

class SayingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saying
        fields = ['id', 'title', 'slug', 'text', 'view', 'author', 'category', 'image', 'is_active', 'created_at', 'updated_at']