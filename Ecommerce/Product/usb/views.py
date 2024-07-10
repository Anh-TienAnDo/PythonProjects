from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import json
from django.views.decorators.csrf import csrf_exempt
from .models import USB
from .serializers import USBSerializer

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

def get_producer_name(usb):
    producer_name = str(usb.producer.name)
    return producer_name

def get_type_name(usb):
    type_name = str(usb.type.name)
    return type_name

class USBView(APIView):
    def get(self, request):
        start = int(request.GET.get('_start', 0))
        limit = int(request.GET.get('_limit', 12))
        usbs = USB.objects.filter(is_active=True)
        check = check_data_exists(usbs)
        if check[0] is False:
            return Response(check[1])
        total = len(usbs)
        data = []
        for usb in usbs[start:start + limit]:
            usb_serializer = USBSerializer(usb).data
            usb_serializer["producer"] = get_producer_name(usb)
            usb_serializer["type"] = get_type_name(usb)
            data.append(usb_serializer)

        return Response({
                'status': 'Success',
                'status_code': status.HTTP_200_OK,
                'message': 'Data retrieved successfully',
                'data': {
                    'total': total,
                    'usbs': data
                }
            })
        

    def post(self, request):
        serializer = USBSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class USBDetailView(APIView):
    def get(self, request, slug):
        usb = USB.objects.filter(slug=slug).first()
        check = check_data_exists(usb)
        if check[0] is False:
            return Response(check[1])
        usb_serializer = USBSerializer(usb).data
        usb_serializer["producer"] = get_producer_name(usb)
        usb_serializer["type"] = get_type_name(usb)
        return Response({
            'status': 'Success',
            'status_code': status.HTTP_200_OK,
            'message': 'Data retrieved successfully',
            'data': usb_serializer
        })

    def put(self, request, id):
        usb = USB.objects.filter(slug=slug).first()
        check = check_data_exists(usb)
        if check[0] is False:
            return Response(check[1])
        serializer = USBSerializer(usb, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        usb = USB.objects.filter(id=id).first()
        check = check_data_exists(usb)
        if check[0] is False:
            return Response(check[1])
        usb.is_active = False
        return Response({
            'status': 'Success',
            'status_code': status.HTTP_200_OK,
            'message': 'Data deleted successfully',
            'data': None
        })
    

