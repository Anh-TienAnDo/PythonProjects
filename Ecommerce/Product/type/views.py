from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from Product.response import ResponseGenerator

# Create your views here.
def check_data_exists(data):
    if not data:
        return [False, ResponseGenerator.error(message='Data not found')]
    return [True, None]

class TypeView(APIView):
    def get(self, request):
        types = Type.objects.filter(is_active=True)
        check = check_data_exists(types)
        if check[0] is False:
            return check[1]
        data = TypeSerializer(types, many=True).data
        return ResponseGenerator.success(data=data, message='Data retrieved successfully')

    def post(self, request):
        serializer = TypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseGenerator.created(data=serializer.data, message='Type created successfully')
        return ResponseGenerator.error(message=serializer.errors)
    
    def put(self, request, pk):
        type = Type.objects.get(pk=pk)
        if not type:
            return ResponseGenerator.error(message='Type not found')
        serializer = TypeSerializer(type, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return ResponseGenerator.success(data=serializer.data, message='Type updated successfully')
        return ResponseGenerator.error(message=serializer.errors)
    
    def delete(self, request, pk):
        type = Type.objects.get(pk=pk)
        if not type:
            return ResponseGenerator.error(message='Type not found')
        type.delete()
        return ResponseGenerator.deleted(message='Type deleted successfully')
    
    def get_by_slug(self, request, slug):
        type = Type.objects.get(slug=slug)
        if not type:
            return ResponseGenerator.error(message='Type not found')
        data = TypeSerializer(type).data
        return ResponseGenerator.success(data=data, message='Data retrieved successfully')
