from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import json
from django.views.decorators.csrf import csrf_exempt
from .models import USB
from .serializers import USBSerializer
from Product.decorators import authenticate_user, authenticate_staff, authenticate_admin
from Product.utils import slugify

# Create your views here.
def check_data_exists(data):
    if not data:
        return [False, {
            'status': 'Failed',
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
        usbs = USB.objects.filter(is_active=True).order_by('-updated_at')[start:start + limit]
        check = check_data_exists(usbs)
        if check[0] is False:
            return Response(check[1])
        
        total = USB.objects.filter(is_active=True).count()
        usbs_serializer = USBSerializer(usbs, many=True).data

        return Response({
                'status': 'Success',
                'message': 'Data retrieved successfully',
                'data': {
                    'total': total,
                    'usbs': usbs_serializer
                }
            }, status=status.HTTP_200_OK)
        
    @authenticate_staff
    def post(self, request):
        serializer = USBSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class USBDetailView(APIView):
    def get(self, request, slug):
        usb = USB.objects.filter(slug=slug, is_active=True).first()
        check = check_data_exists(usb)
        if check[0] is False:
            return Response(check[1])
        usb.view += 1
        usb.save()
        usb_serializer = USBSerializer(usb).data
        usb_serializer["producer"] = get_producer_name(usb)
        usb_serializer["type"] = get_type_name(usb)
        return Response({
            'status': 'Success',
            'message': 'Data retrieved successfully',
            'data': usb_serializer
        }, status=status.HTTP_200_OK)

    @authenticate_staff
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

    @authenticate_staff
    def delete(self, request, id):
        usb = USB.objects.filter(id=id).first()
        check = check_data_exists(usb)
        if check[0] is False:
            return Response(check[1])
        usb.is_active = False
        return Response({
            'status': 'Success',
            'message': 'Data deleted successfully',
            'data': None
        }, status=status.HTTP_200_OK)
    
      
class USBSearchAndFilterView(APIView):
    def get(self, request):
        query = str(request.GET.get('query', ""))
        query = slugify(query)
        producer = str(request.GET.get('producer', ""))
        type_usb = str(request.GET.get('type_usb', ""))
        price_new = int(request.GET.get('price', 0))
        start = int(request.GET.get('_start', 0))
        limit = int(request.GET.get('_limit', 12))
        
        usbs = USB.objects.filter(slug__icontains=query, producer__slug__contains=producer, type__slug__contains=type_usb, price_new__gte=price_new, is_active=True).order_by('-updated_at')[start:start + limit]
        check = check_data_exists(usbs)
        if check[0] is False:
            return Response(check[1])
        
        total = USB.objects.filter(slug__icontains=query, producer__slug__contains=producer, type__slug__contains=type_usb, price_new__gte=price_new, is_active=True).count()
        usbs_serializer = USBSerializer(usbs, many=True).data
        
        return Response({
            'status': 'Success',
            'message': 'Data retrieved successfully',
            'data': {
                'total': total,
                'usbs': usbs_serializer
            }
        }, status=status.HTTP_200_OK)
        
class USBFilterView(APIView):
    def get(self, request):
        producer = str(request.GET.get('producer', ""))
        type_usb = str(request.GET.get('type_usb', ""))
        price_new = int(request.GET.get('price', 0))
        start = int(request.GET.get('_start', 0))
        limit = int(request.GET.get('_limit', 12))
        
        usbs = USB.objects.filter(producer__slug__contains=producer, type__slug__contains=type_usb, price_new__gte=price_new, is_active=True).order_by('-updated_at')[start:start + limit]
        check = check_data_exists(usbs)
        if check[0] is False:
            return Response(check[1])
        
        total = USB.objects.filter(producer__slug__contains=producer, type__slug__contains=type_usb, price_new__gte=price_new, is_active=True).count()
        usbs_serializer = USBSerializer(usbs, many=True).data
        
        return Response({
            'status': 'Success',
            'message': 'Data retrieved successfully',
            'data': {
                'total': total,
                'usbs': usbs_serializer
            }
        }, status=status.HTTP_200_OK)

