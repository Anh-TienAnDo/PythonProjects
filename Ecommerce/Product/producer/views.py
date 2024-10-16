from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

# Create your views here.
def check_data_exists(data):
    if not data:
        return [False, {
            'status': 'Failed',
            'message': 'Data not found',
            'data': None
        }]
    return [True, None]

class ProducerView(APIView):
    def get(self, request):
        producers = Producer.objects.filter(is_active=True)
        check = check_data_exists(producers)
        if check[0] is False:
            return Response(check[1])
        data = ProducerSerializer(producers, many=True).data
        return Response({
            'status': 'Success',
            'message': 'Data retrieved successfully',
            'data': data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProducerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class ProducerByTypeView(APIView):
#     def get(self, request):
#         type_product = request.GET.get('type_product', 'loudspeaker')
#         producers = Producer.objects.filter(type_product=type_product, is_active=True)
#         check = check_data_exists(producers)
#         if check[0] is False:
#             return Response(check[1])
#         data = ProducerSerializer(producers, many=True).data
#         return Response({
#             'status': 'Success',
#             'message': 'Data retrieved successfully',
#             'data': data
#         }, status=status.HTTP_200_OK)
