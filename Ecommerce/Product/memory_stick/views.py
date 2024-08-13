from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import json
from django.views.decorators.csrf import csrf_exempt
from .models import MemoryStick
from .serializers import MemoryStickSerializer
from Product.decorators import authenticate_user, authenticate_staff, authenticate_admin

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
        print("Getting all memory sticks")
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
        
    @authenticate_staff
    def post(self, request):
        serializer = MemoryStickSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MemoryStickDetailView(APIView):
    def get(self, request, slug):
        print("Getting memory stick by slug")
        memory_stick = MemoryStick.objects.filter(slug=slug).first()
        check = check_data_exists(memory_stick)
        if check[0] is False:
            return Response(check[1])
        memory_stick.view += 1
        memory_stick.save()
        memory_stick_serializer = MemoryStickSerializer(memory_stick).data
        memory_stick_serializer["producer"] = get_producer_name(memory_stick)
        memory_stick_serializer["type"] = get_type_name(memory_stick)
        return Response({
            'status': 'Success',
            'status_code': status.HTTP_200_OK,
            'message': 'Data retrieved successfully',
            'data': memory_stick_serializer
        })

    @authenticate_staff
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

    @authenticate_staff
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
    
class MemoryStickSearchByProducerView(APIView):
    def get(self, request):
        print("Searching memory stick by producer")
        start = int(request.GET.get('_start', 0))
        limit = int(request.GET.get('_limit', 12))
        query = str(request.GET.get('_query', ''))
        memory_sticks = MemoryStick.objects.filter(producer__name__icontains=query, is_active=True).order_by('-created_at')[start:start+limit]
        check = check_data_exists(memory_sticks)
        if check[0] is False:
            return Response(check[1])
        data = []
        for memory_stick in memory_sticks:
            memory_stick_serializer = MemoryStickSerializer(memory_stick).data
            memory_stick_serializer["producer"] = get_producer_name(memory_stick)
            memory_stick_serializer["type"] = get_type_name(memory_stick)
            data.append(memory_stick_serializer)
        return Response({
            'status': 'Success',
            'status_code': status.HTTP_200_OK,
            'message': 'Data retrieved successfully',
            'data': data
        })

class MemoryStickSearchByNameView(APIView):
    def get(self, request):
        print("Searching memory stick by name")
        start = int(request.GET.get('_start', 0))
        limit = int(request.GET.get('_limit', 12))
        query = str(request.GET.get('_query', ''))
        memory_sticks = MemoryStick.objects.filter(name__icontains=query, is_active=True).order_by('-created_at')[start:start+limit]
        check = check_data_exists(memory_sticks)
        if check[0] is False:
            return Response(check[1])
        data = []
        for memory_stick in memory_sticks:
            memory_stick_serializer = MemoryStickSerializer(memory_stick).data
            memory_stick_serializer["producer"] = get_producer_name(memory_stick)
            memory_stick_serializer["type"] = get_type_name(memory_stick)
            data.append(memory_stick_serializer)
        return Response({
            'status': 'Success',
            'status_code': status.HTTP_200_OK,
            'message': 'Data retrieved successfully',
            'data': data
        })
        
class MemoryStickFilterView(APIView):
    def get(self, request):
        print("Filtering memory stick")
        start = int(request.GET.get('_start', 0))
        limit = int(request.GET.get('_limit', 12))
        producer = str(request.GET.get('_producer', 'all'))
        type_memorystick = str(request.GET.get('_type', 'all'))
        price_new = str(request.GET.get('_price', 'all'))
        price_range = price_new.split("-")
        if producer != 'all' and type_memorystick != 'all' and price != 'all':
            memory_sticks = MemoryStick.objects.filter(producer__name__icontains=producer, type__name__icontains=type_memorystick, price_new__gte=price_range[0], price_new__lte=price_range[1], is_active=True).order_by('-created_at')
        elif producer != 'all' and type_memorystick != 'all':
            memory_sticks = MemoryStick.objects.filter(producer__name__icontains=producer, type__name__icontains=type_memorystick, is_active=True).order_by('-created_at')
        elif producer != 'all' and price_new != 'all':
            memory_sticks = MemoryStick.objects.filter(producer__name__icontains=producer, price_new__gte=price_range[0], price_new__lte=price_range[1], is_active=True).order_by('-created_at')
        elif type_memorystick != 'all' and price_new != 'all':
            memory_sticks = MemoryStick.objects.filter(type__name__icontains=type_memorystick, price_new__gte=price_range[0], price_new__lte=price_range[1], is_active=True).order_by('-created_at')
        elif producer != 'all':
            memory_sticks = MemoryStick.objects.filter(producer__name__icontains=producer, is_active=True).order_by('-created_at')
        elif type_memorystick != 'all':
            memory_sticks = MemoryStick.objects.filter(type__name__icontains=type_memorystick, is_active=True).order_by('-created_at')
        elif price_new != 'all':
            memory_sticks = MemoryStick.objects.filter(price_new__gte=price_range[0], price_new__lte=price_range[1], is_active=True).order_by('-created_at')
        else:
            memory_sticks = MemoryStick.objects.filter(is_active=True).order_by('-created_at')
        check = check_data_exists(memory_sticks)
        if check[0] is False:
            return Response(check[1])
        total = len(memory_sticks)
        data = []
        for memory_stick in memory_sticks[start:start+limit]:
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

