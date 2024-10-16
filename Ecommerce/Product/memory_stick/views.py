from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.views.generic import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import MemoryStick
from .serializers import MemoryStickSerializer
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

def get_producer_name(memory_stick):
    producer_name = str(memory_stick.producer.name)
    return producer_name

def get_type_name(memory_stick):
    type_name = str(memory_stick.type.name)
    return type_name

class MemoryStickView(View):
    # @authenticate_user
    def get(self, request):
        print("Getting all memory_sticks")
        start = int(request.GET.get('_start', 0))
        limit = int(request.GET.get('_limit', 12))
        memory_sticks = MemoryStick.objects.filter(is_active=True).order_by('-updated_at')[start:start + limit]
        check = check_data_exists(memory_sticks)
        if check[0] is False:
            return JsonResponse(check[1])
        
        total =  MemoryStick.objects.filter(is_active=True).count()
        memory_sticks_serializer = MemoryStickSerializer(memory_sticks, many=True).data

        return JsonResponse({
                'status': 'Success',
                'message': 'Data retrieved successfully',
                'data': {
                    'total': total,
                    'memory_sticks': memory_sticks_serializer
                }
            }, safe=False, status=status.HTTP_200_OK)
        
    @authenticate_staff
    def post(self, request):
        serializer = MemoryStickSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MemoryStickDetailView(View):
    # @authenticate_user
    def get(self, request, slug):
        print("Getting memory_stick by slug")
        memory_stick = MemoryStick.objects.filter(slug=slug, is_active=True).first()
        check = check_data_exists(memory_stick)
        if check[0] is False:
            return JsonResponse(check[1])
        memory_stick.view += 1
        memory_stick.save()
        memory_stick_serializer = MemoryStickSerializer(memory_stick).data
        memory_stick_serializer["producer"] = get_producer_name(memory_stick)
        memory_stick_serializer["type"] = get_type_name(memory_stick)
        return JsonResponse({
            'status': 'Success',
            'message': 'Data retrieved successfully',
            'data': memory_stick_serializer
        }, status=status.HTTP_200_OK)

    @authenticate_staff
    def put(self, request, id):
        memory_stick = MemoryStick.objects.filter(id=id, is_active=True).first()
        check = check_data_exists(memory_stick)
        if check[0] is False:
            return Response(check[1])
        serializer = MemoryStickSerializer(memory_stick, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @authenticate_staff
    def delete(self, request, id):
        memory_stick = MemoryStick.objects.filter(id=id, is_active=True).first()
        check = check_data_exists(memory_stick)
        if check[0] is False:
            return JsonResponse(check[1])
        memory_stick.is_active = False
        memory_stick.save()
        return JsonResponse({
            'status': 'Success',
            'status_code': status.HTTP_200_OK,
            'message': 'Data deleted successfully',
            'data': None
        })
        
class MemoryStickSearchAndFilterView(View):
    # @authenticate_user
    def get(self, request):
        print('Looking for memory_sticks by name')
        query = str(request.GET.get('query', ""))
        query = slugify(query)
        producer = str(request.GET.get('producer', ""))
        type_memory_stick = str(request.GET.get('type_memory', ""))
        price_new = int(request.GET.get('price', 0))
        start = int(request.GET.get('_start', 0))
        limit = int(request.GET.get('_limit', 12))
        memory_sticks = MemoryStick.objects.filter(slug__icontains=query, producer__slug__contains=producer, type__slug__contains=type_memory_stick, price_new__gte=price_new, is_active=True).order_by('-updated_at')[start:start + limit]
        check = check_data_exists(memory_sticks)
        if check[0] is False:
            return JsonResponse(check[1])
        total = MemoryStick.objects.filter(slug__icontains=query, producer__slug__contains=producer, type__slug__contains=type_memory_stick, price_new__gte=price_new, is_active=True).count()
        memory_sticks_serializer = MemoryStickSerializer(memory_sticks, many=True).data
        
        return JsonResponse({
                'status': 'Success',
                'message': 'Data retrieved successfully',
                'data': {
                    'total': total,
                    'memory_sticks': memory_sticks_serializer
                }
            }, safe=False, status=status.HTTP_200_OK)
        
  
class MemoryStickFilterView(View):
    # @authenticate_user
    def get(self, request):
        print("Filtering memory_sticks")
        producer = str(request.GET.get('producer', ""))
        type_memory_stick = str(request.GET.get('type_memory', ""))
        price_new = int(request.GET.get('price', 0))
        start = int(request.GET.get('_start', 0))
        limit = int(request.GET.get('_limit', 12))
        
        memory_sticks = MemoryStick.objects.filter(producer__slug__contains=producer, type__slug__contains=type_memory_stick, price_new__gte=price_new, is_active=True).order_by('-updated_at')[start:start + limit]
        check = check_data_exists(memory_sticks)
        if check[0] is False:
            return JsonResponse(check[1])
        total = MemoryStick.objects.filter(producer__slug__contains=producer, type__slug__contains=type_memory_stick, price_new__gte=price_new, is_active=True).count()
        memory_sticks_serializer = MemoryStickSerializer(memory_sticks, many=True).data

        return JsonResponse({
                'status': 'Success',
                'message': 'Data retrieved successfully',
                'data': {
                    'total': total,
                    'memory_sticks': memory_sticks_serializer
                }
            }, safe=False, status=status.HTTP_200_OK)
   
