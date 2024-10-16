from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.views import APIView
from django.views.generic import View
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import LoudSpeaker
from .serializers import LoudspeakerSerializer
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
            return JsonResponse(check[1])
        
        total =  LoudSpeaker.objects.filter(is_active=True).count()
        loudspeakers_serializer = LoudspeakerSerializer(loudspeakers, many=True).data

        return JsonResponse({
                'status': 'Success',
                'message': 'Data retrieved successfully',
                'data': {
                    'total': total,
                    'loudspeakers': loudspeakers_serializer
                }
            }, safe=False, status=status.HTTP_200_OK)
        
    @authenticate_staff
    def post(self, request):
        serializer = LoudspeakerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoudspeakerDetailView(View):
    # @authenticate_user
    def get(self, request, slug):
        print("Getting loudspeaker by slug")
        loudspeaker = LoudSpeaker.objects.filter(slug=slug, is_active=True).first()
        check = check_data_exists(loudspeaker)
        if check[0] is False:
            return JsonResponse(check[1])
        loudspeaker.view += 1
        loudspeaker.save()
        loudspeaker_serializer = LoudspeakerSerializer(loudspeaker).data
        loudspeaker_serializer["producer"] = get_producer_name(loudspeaker)
        loudspeaker_serializer["type"] = get_type_name(loudspeaker)
        return JsonResponse({
            'status': 'Success',
            'message': 'Data retrieved successfully',
            'data': loudspeaker_serializer
        }, status=status.HTTP_200_OK)

    @authenticate_staff
    def put(self, request, id):
        loudspeaker = LoudSpeaker.objects.filter(id=id, is_active=True).first()
        check = check_data_exists(loudspeaker)
        if check[0] is False:
            return Response(check[1])
        serializer = LoudspeakerSerializer(loudspeaker, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @authenticate_staff
    def delete(self, request, id):
        loudspeaker = LoudSpeaker.objects.filter(id=id, is_active=True).first()
        check = check_data_exists(loudspeaker)
        if check[0] is False:
            return JsonResponse(check[1])
        loudspeaker.is_active = False
        loudspeaker.save()
        return JsonResponse({
            'status': 'Success',
            'status_code': status.HTTP_200_OK,
            'message': 'Data deleted successfully',
            'data': None
        })
        
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
            return JsonResponse(check[1])
        total = LoudSpeaker.objects.filter(slug__icontains=query, producer__slug__contains=producer, type__slug__contains=type_loudspeaker, price_new__gte=price_new, is_active=True).count()
        loudspeakers_serializer = LoudspeakerSerializer(loudspeakers, many=True).data
        
        return JsonResponse({
                'status': 'Success',
                'message': 'Data retrieved successfully',
                'data': {
                    'total': total,
                    'loudspeakers': loudspeakers_serializer
                }
            }, safe=False, status=status.HTTP_200_OK)
        
  
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
            return JsonResponse(check[1])
        total = LoudSpeaker.objects.filter(producer__slug__contains=producer, type__slug__contains=type_loudspeaker, price_new__gte=price_new, is_active=True).count()
        loudspeakers_serializer = LoudspeakerSerializer(loudspeakers, many=True).data

        return JsonResponse({
                'status': 'Success',
                'message': 'Data retrieved successfully',
                'data': {
                    'total': total,
                    'loudspeakers': loudspeakers_serializer
                }
            }, safe=False, status=status.HTTP_200_OK)
   
