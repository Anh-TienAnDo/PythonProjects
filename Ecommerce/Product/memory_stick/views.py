from django.shortcuts import render
from rest_framework import status
from django.views.generic import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import MemoryStick
from .serializers import MemoryStickSerializer
from Product.decorators import authenticate_user, authenticate_staff, authenticate_admin
from Product.utils import slugify
from Product.response import ResponseGenerator

# Create your views here.
def check_data_exists(data):
    if not data:
        return [False, ResponseGenerator.error(message='Data not found')]
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
            return ResponseGenerator.error(data={
                "total": 0,
                "memory_sticks": []
            }, message='Data not found')
        
        total =  MemoryStick.objects.filter(is_active=True).count()
        memory_sticks_serializer = MemoryStickSerializer(memory_sticks, many=True).data

        return ResponseGenerator.success(data={
            'total': total,
            'memory_sticks': memory_sticks_serializer
        }, message='Data retrieved successfully')
        
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
            return check[1]
        memory_stick.view += 1
        memory_stick.save()
        memory_stick_serializer = MemoryStickSerializer(memory_stick).data
        memory_stick_serializer["producer"] = get_producer_name(memory_stick)
        memory_stick_serializer["type"] = get_type_name(memory_stick)
        return ResponseGenerator.success(data=memory_stick_serializer, message='Data retrieved successfully')

    @authenticate_staff
    def put(self, request, id):
        memory_stick = MemoryStick.objects.filter(id=id, is_active=True).first()
        check = check_data_exists(memory_stick)
        if check[0] is False:
            return check[1]
        serializer = MemoryStickSerializer(memory_stick, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseGenerator.success(data=serializer.data, message='Data updated successfully')
        return ResponseGenerator.error(message=serializer.errors)

    @authenticate_staff
    def delete(self, request, id):
        memory_stick = MemoryStick.objects.filter(id=id, is_active=True).first()
        check = check_data_exists(memory_stick)
        if check[0] is False:
            return check[1]
        memory_stick.is_active = False
        memory_stick.save()
        return ResponseGenerator.deleted(message='Data deleted successfully')
        
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
            return ResponseGenerator.error(data={
                "total": 0,
                "memory_sticks": []
            }, message='Data not found')
        total = MemoryStick.objects.filter(slug__icontains=query, producer__slug__contains=producer, type__slug__contains=type_memory_stick, price_new__gte=price_new, is_active=True).count()
        memory_sticks_serializer = MemoryStickSerializer(memory_sticks, many=True).data
        
        return ResponseGenerator.success(data={
            'total': total,
            'memory_sticks': memory_sticks_serializer
        }, message='Data retrieved successfully')
        
  
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
            return ResponseGenerator.error(data={
                "total": 0,
                "memory_sticks": []
            }, message='Data not found')
        total = MemoryStick.objects.filter(producer__slug__contains=producer, type__slug__contains=type_memory_stick, price_new__gte=price_new, is_active=True).count()
        memory_sticks_serializer = MemoryStickSerializer(memory_sticks, many=True).data

        return ResponseGenerator.success(data={
            'total': total,
            'memory_sticks': memory_sticks_serializer
        }, message='Data retrieved successfully')
   
