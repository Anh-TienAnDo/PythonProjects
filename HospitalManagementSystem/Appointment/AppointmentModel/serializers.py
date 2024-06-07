from rest_framework import serializers
from .models import *

class AppointmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = ['id', 'doctor', 'patient', 'appointment_date_time', 'place_of_examination', 'is_active', 'description']

    def create(self, validated_data):
        return Appointments.objects.create(**validated_data)