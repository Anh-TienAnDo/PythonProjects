from django.shortcuts import render
from rest_framework import status
from django.views.generic import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import LoudSpeaker
from .serializers import LoudspeakerSerializer
from Product.decorators import authenticate_user, authenticate_staff, authenticate_admin
from Product.utils import slugify
from Product.response import ResponseGenerator

# Create your views here.
def check_data_exists(data):
    if not data:
        return [False, ResponseGenerator.error(message='Data not found')]
    return [True, None]

def get_producer_name(loudspeaker):
    producer_name = str(loudspeaker.producer.name)
    return producer_name

def get_type_name(loudspeaker):
    type_name = str(loudspeaker.type.name)
    return type_name

class LoudspeakerView(View):
    # @authenticate_user
    def get(self, request):
        print("Getting all loudspeakers")
        start = int(request.GET.get('_start', 0))
        limit = int(request.GET.get('_limit', 12))
        loudspeakers = LoudSpeaker.objects.filter(is_active=True).order_by('-updated_at')[start:start + limit]
        check = check_data_exists(loudspeakers)
        if check[0] is False:
            return ResponseGenerator.error(data={
                "total": 0,
                "loudspeakers": []
            }, message='Data not found')
        
        total =  LoudSpeaker.objects.filter(is_active=True).count()
        loudspeakers_serializer = LoudspeakerSerializer(loudspeakers, many=True).data

        return ResponseGenerator.success(data={
            'total': total,
            'loudspeakers': loudspeakers_serializer
        }, message='Data retrieved successfully')
        
    @authenticate_staff
    def post(self, request):
        serializer = LoudspeakerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseGenerator.created(data=serializer.data, message='Loudspeaker created successfully')
        return ResponseGenerator.error(message=serializer.errors)
    
class LoudspeakerDetailView(View):
    def get(self, request, slug):
        loudspeaker = LoudSpeaker.objects.filter(slug=slug, is_active=True).first()
        check = check_data_exists(loudspeaker)
        if check[0] is False:
            return check[1]
        loudspeaker.view += 1
        loudspeaker.save()
        data = LoudspeakerSerializer(loudspeaker).data
        data['producer'] = get_producer_name(loudspeaker)
        data['type'] = get_type_name(loudspeaker)
        return ResponseGenerator.success(data=data, message='Data retrieved successfully')
    
    @authenticate_staff
    def put(self, request, slug):
        loudspeaker = LoudSpeaker.objects.filter(slug=slug, is_active=True).first()
        check = check_data_exists(loudspeaker)
        if check[0] is False:
            return check[1]
        serializer = LoudspeakerSerializer(loudspeaker, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return ResponseGenerator.success(data=serializer.data, message='Loudspeaker updated successfully')
        return ResponseGenerator.error(message=serializer.errors)
    
    @authenticate_staff
    def delete(self, request, slug):
        loudspeaker = LoudSpeaker.objects.filter(slug=slug, is_active=True).first()
        check = check_data_exists(loudspeaker)
        if check[0] is False:
            return check[1]
        loudspeaker.delete()
        return ResponseGenerator.deleted(message='Loudspeaker deleted successfully')

class LoudspeakerSearchAndFilterView(View):
    # @authenticate_user
    def get(self, request):
        print('Looking for loudspeakers by name')
        query = str(request.GET.get('query', ""))
        query = slugify(query)
        producer = str(request.GET.get('producer', ""))
        type_loudspeaker = str(request.GET.get('type_loudspeaker', ""))
        price_new = int(request.GET.get('price', 0))
        start = int(request.GET.get('_start', 0))
        limit = int(request.GET.get('_limit', 12))
        loudspeakers = LoudSpeaker.objects.filter(slug__icontains=query, producer__slug__contains=producer, type__slug__contains=type_loudspeaker, price_new__gte=price_new, is_active=True).order_by('-updated_at')[start:start + limit]
        check = check_data_exists(loudspeakers)
        if check[0] is False:
            return ResponseGenerator.error(data={
                "total": 0,
                "loudspeakers": []
            }, message='Data not found')
        total = LoudSpeaker.objects.filter(slug__icontains=query, producer__slug__contains=producer, type__slug__contains=type_loudspeaker, price_new__gte=price_new, is_active=True).count()
        loudspeakers_serializer = LoudspeakerSerializer(loudspeakers, many=True).data
        
        return ResponseGenerator.success(data={
            'total': total,
            'loudspeakers': loudspeakers_serializer
        }, message='Data retrieved successfully')
        
  
class LoudspeakerFilterView(View):
    # @authenticate_user
    def get(self, request):
        print("Filtering loudspeakers")
        producer = str(request.GET.get('producer', ""))
        type_loudspeaker = str(request.GET.get('type_loudspeaker', ""))
        price_new = int(request.GET.get('price', 0))
        start = int(request.GET.get('_start', 0))
        limit = int(request.GET.get('_limit', 12))
        
        loudspeakers = LoudSpeaker.objects.filter(producer__slug__contains=producer, type__slug__contains=type_loudspeaker, price_new__gte=price_new, is_active=True).order_by('-updated_at')[start:start + limit]
        check = check_data_exists(loudspeakers)
        if check[0] is False:
            return ResponseGenerator.error(data={
                "total": 0,
                "loudspeakers": []
            }, message='Data not found')
        total = LoudSpeaker.objects.filter(producer__slug__contains=producer, type__slug__contains=type_loudspeaker, price_new__gte=price_new, is_active=True).count()
        loudspeakers_serializer = LoudspeakerSerializer(loudspeakers, many=True).data

        return ResponseGenerator.success(data={
            'total': total,
            'loudspeakers': loudspeakers_serializer
        }, message='Data retrieved successfully')
   
