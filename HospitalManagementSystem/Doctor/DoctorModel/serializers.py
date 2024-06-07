from rest_framework import serializers
from .models import Doctor, Name, Address, Specialty, Level, PlaceWork

class NameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Name
        fields = ['fname', 'lname', 'fullname']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'district', 'city', 'note']

class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['name', 'slug', 'description', 'is_active']

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['name', 'slug', 'description', 'is_active']

class PlaceWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceWork
        fields = ['name', 'slug', 'description', 'is_active']

class DoctorSerializer(serializers.ModelSerializer):
    name = NameSerializer()
    address = AddressSerializer()
    specialties = SpecialtySerializer(many=True)
    level = LevelSerializer()
    place_of_work = PlaceWorkSerializer()

    class Meta:
        model = Doctor
        fields = "__all__"
