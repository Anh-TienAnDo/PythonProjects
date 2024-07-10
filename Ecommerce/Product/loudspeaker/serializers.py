from rest_framework import serializers
from .models import LoudSpeaker

class LoudspeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoudSpeaker
        fields = ['id', 'name', 'slug', 'power', 'view', 'producer', 'type', 'image', 'price_old', 'price_new', 'description']