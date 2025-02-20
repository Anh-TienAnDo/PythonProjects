from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Producer
from .serializers import ProducerSerializer
from Product.response import ResponseGenerator

# Create your views here.
def check_data_exists(data):
    if not data:
        return [False, ResponseGenerator.error(message='Data not found')]
    return [True, None]

class ProducerView(APIView):
    def get(self, request):
        producers = Producer.objects.filter(is_active=True)
        check = check_data_exists(producers)
        if check[0] is False:
            return check[1]
        data = ProducerSerializer(producers, many=True).data
        return ResponseGenerator.success(data=data, message='Data retrieved successfully')

    def post(self, request):
        serializer = ProducerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseGenerator.created(data=serializer.data, message='Producer created successfully')
        return ResponseGenerator.error(message=serializer.errors)
    
    def put(self, request, pk):
        producer = Producer.objects.get(pk=pk)
        if not producer:
            return ResponseGenerator.error(message='Producer not found')
        serializer = ProducerSerializer(producer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return ResponseGenerator.success(data=serializer.data, message='Producer updated successfully')
        return ResponseGenerator.error(message=serializer.errors)
    
    def delete(self, request, pk):
        producer = Producer.objects.get(pk=pk)
        if not producer:
            return ResponseGenerator.error(message='Producer not found')
        producer.delete()
        return ResponseGenerator.deleted(message='Producer deleted successfully')
    
    def get_by_slug(self, request, slug):
        producer = Producer.objects.get(slug=slug)
        if not producer:
            return ResponseGenerator.error(message='Producer not found')
        data = ProducerSerializer(producer).data
        return ResponseGenerator.success(data=data, message='Data retrieved successfully')
    
