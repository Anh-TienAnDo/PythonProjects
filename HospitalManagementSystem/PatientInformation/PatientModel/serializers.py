from rest_framework import serializers
from .models import Name, Address, PatientInformation, HistoryMedical

class NameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Name
        fields = ['fname', 'lname', 'fullname']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'district', 'city', 'note']

class PatientInformationSerializer(serializers.ModelSerializer):
    name = NameSerializer()
    address = AddressSerializer()

    class Meta:
        model = PatientInformation
        fields = ['id', 'name', 'day_of_birth', 'gender', 'address', 'phone','is_active']

    def create(self, validated_data):
        name_data = validated_data.pop('name')
        address_data = validated_data.pop('address')
        name = Name.objects.create(**name_data)
        address = Address.objects.create(**address_data)
        patient_information = PatientInformation.objects.create(name=name, address=address, **validated_data)
        return patient_information

    def update(self, instance, validated_data):
        name_data = validated_data.pop('name')
        address_data = validated_data.pop('address')

        instance.name.fname = name_data.get('fname', instance.name.fname)
        instance.name.lname = name_data.get('lname', instance.name.lname)
        instance.name.fullname = f"{instance.name.lname} {instance.name.fname}"
        instance.name.save()

        instance.address.street = address_data.get('street', instance.address.street)
        instance.address.district = address_data.get('district', instance.address.district)
        instance.address.city = address_data.get('city', instance.address.city)
        instance.address.note = address_data.get('note', instance.address.note)
        instance.address.save()

        instance.day_of_birth = validated_data.get('day_of_birth', instance.day_of_birth)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()

        return instance

class HistoryMedicalSerializer(serializers.ModelSerializer):
    patient_information = PatientInformationSerializer()

    class Meta:
        model = HistoryMedical
        fields = ['id', 'patient_information', 'doctor', 'place_of_examination', 'pathology', 'treatment', 'cost', 'paymented', 'is_active', 'description', 'evaluation']

    # def create(self, validated_data):
    #     return HistoryMedical.objects.create(**validated_data)

    def update(self, instance, validated_data):
        patient_information_data = validated_data.pop('patient_information')
        patient_information_serializer = PatientInformationSerializer(instance.patient_information, data=patient_information_data)
        if patient_information_serializer.is_valid():
            patient_information_serializer.save()

        instance.doctor = validated_data.get('doctor', instance.doctor)
        instance.place_of_examination = validated_data.get('place_of_examination', instance.place_of_examination)
        instance.pathology = validated_data.get('pathology', instance.pathology)
        instance.treatment = validated_data.get('treatment', instance.treatment)
        instance.cost = validated_data.get('cost', instance.cost)
        instance.paymented = validated_data.get('paymented', instance.paymented)
        instance.description = validated_data.get('description', instance.description)
        instance.evaluation = validated_data.get('evaluation', instance.evaluation)
        instance.save()

        return instance
