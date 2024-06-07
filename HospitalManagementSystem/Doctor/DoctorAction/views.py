from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView # Import the missing APIView class
from DoctorModel.models import *
from DoctorModel.serializers import *
import json
from django.views.decorators.csrf import csrf_exempt, csrf_protect

class DoctorViewSet(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = response.data
        for d in data:
            if d['is_active'] == False:
                data.remove(d)
        return Response(
            {
                'status': 'Success',
                'status_code': '200',
                'message': 'Get all users successful!',
                'data': data,
            }
        )
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                'status': 'Success',
                'status_code': '201',
                'message': 'Create user successful!',
            }
        )
    
class DoctorRetrieveUpdateDestroyAPIViewID(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    lookup_field = "id"
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response(
            {
                'status': 'Success',
                'status_code': '200',
                'message': 'Get user successful!',
                'data': response.data,
            }
        )
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return Response(
            {
                'status': 'Success',
                'status_code': '200',
                'message': 'Delete user successful!',
            }
        )

class DoctorCreate(APIView):
    @csrf_exempt
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            # Create or get Name
            name_data = data.get('name')
            name, created = Name.objects.get_or_create(
                fname=name_data['fname'], 
                lname=name_data['lname'],
                defaults={'fullname': name_data['fullname']}
            )
            
            # Create or get Address
            address_data = data.get('address')
            address, created = Address.objects.get_or_create(
                street=address_data['street'], 
                district=address_data['district'], 
                city=address_data['city'],
                defaults={'note': address_data.get('note', '')}
            )
            
            # Get or create Level
            level_data = data.get('level')
            level, created = Level.objects.get_or_create(
                name=level_data['name'],
                defaults={
                    'slug': level_data['slug'],
                    'description': level_data.get('description', ''),
                    'is_active': level_data.get('is_active', True)
                }
            )
            
            # Get or create PlaceWork
            place_work_data = data.get('place_of_work')
            place_work, created = PlaceWork.objects.get_or_create(
                name=place_work_data['name'],
                defaults={
                    'slug': place_work_data['slug'],
                    'description': place_work_data.get('description', ''),
                    'is_active': place_work_data.get('is_active', True)
                }
            )
            
            # Create Doctor
            doctor = Doctor.objects.create(
                name=name,
                email=data.get('email'),
                image=data.get('image', ''),
                year_of_birth=data.get('year_of_birth'),
                address=address,
                phone=data.get('phone'),
                level=level,
                salary=data.get('salary'),
                place_of_work=place_work,
                year_of_work=data.get('year_of_work'),
                is_active=data.get('is_active', True),
                description=data.get('description', '')
            )
            
            # Add specialties to doctor
            specialties_data = data.get('specialties', [])
            for specialty_data in specialties_data:
                specialty, created = Specialty.objects.get_or_create(
                    name=specialty_data['name'],
                    defaults={
                        'slug': specialty_data['slug'],
                        'description': specialty_data.get('description', ''),
                        'is_active': specialty_data.get('is_active', True)
                    }
                )
                doctor.specialties.add(specialty)
            
            doctor.save()
            
            return Response({"message": "Doctor created successfully"}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class DoctorDelete(APIView):
    @csrf_exempt
    def get(self, request, id):
        try:
            doctor = Doctor.objects.get(id=id)
            doctor.is_active = False
            doctor.save()
            return Response({'status': 'Success', "message": "Doctor deleted successfully"}, status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response({'status': 'Failed', "message": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status': 'Failed', "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
