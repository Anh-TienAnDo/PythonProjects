from rest_framework import serializers
from .models import AudioBook, BookSection

class AudioBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioBook
        fields = ['id', 'title', 'slug', 'view', 'author', 'categories', 'producer', 'description', 'image', 'quantity', 'time_total']

class BookSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookSection
        fields = ['id', 'title', 'slug', 'audio_book', 'url', 'file_type', 'description', 'time']