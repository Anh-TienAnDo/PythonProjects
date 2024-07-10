from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import json
from django.views.decorators.csrf import csrf_exempt
from .models import MemoryStick
from .serializers import MemoryStickSerializer

# Create your views here.
def check_data_exists(data):
    if not data:
        return [False, {
            'status': 'Failed',
            'status_code': status.HTTP_404_NOT_FOUND,
            'message': 'Data not found',
            'data': None
        }]
    return [True, None]

def get_producer_name(memory_stick):
    producer_name = str(memory_stick.producer.name)
    return producer_name

def get_type_name(memory_stick):
    type_name = str(memory_stick.type.name)
    return type_name

class MemoryStickView(APIView):
    def get(self, request):
        start = int(request.GET.get('_start', 0))
        limit = int(request.GET.get('_limit', 12))
        memory_sticks = MemoryStick.objects.filter(is_active=True)
        check = check_data_exists(memory_sticks)
        if check[0] is False:
            return Response(check[1])
        total = len(memory_sticks)
        data = []
        for memory_stick in memory_sticks[start:start + limit]:
            memory_stick_serializer = MemoryStickSerializer(memory_stick).data
            memory_stick_serializer["producer"] = get_producer_name(memory_stick)
            memory_stick_serializer["type"] = get_type_name(memory_stick)
            data.append(memory_stick_serializer)

        return Response({
                'status': 'Success',
                'status_code': status.HTTP_200_OK,
                'message': 'Data retrieved successfully',
                'data': {
                    'total': total,
                    'memory_sticks': data
                }
            })
        

    def post(self, request):
        serializer = MemoryStickSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MemoryStickDetailView(APIView):
    def get(self, request, slug):
        memory_stick = MemoryStick.objects.filter(slug=slug).first()
        check = check_data_exists(memory_stick)
        if check[0] is False:
            return Response(check[1])
        memory_stick_serializer = MemoryStickSerializer(memory_stick).data
        memory_stick_serializer["producer"] = get_producer_name(memory_stick)
        memory_stick_serializer["type"] = get_type_name(memory_stick)
        return Response({
            'status': 'Success',
            'status_code': status.HTTP_200_OK,
            'message': 'Data retrieved successfully',
            'data': memory_stick_serializer
        })

    def put(self, request, slug):
        memory_stick = MemoryStick.objects.filter(slug=slug).first()
        check = check_data_exists(memory_stick)
        if check[0] is False:
            return Response(check[1])
        serializer = MemoryStickSerializer(memory_stick, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        memory_stick = MemoryStick.objects.filter(id=id).first()
        check = check_data_exists(memory_stick)
        if check[0] is False:
            return Response(check[1])
        memory_stick.is_active = False
        return Response({
            'status': 'Success',
            'status_code': status.HTTP_200_OK,
            'message': 'Data deleted successfully',
            'data': None
        })
    
