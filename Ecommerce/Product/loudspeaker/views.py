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

def get_producer_name(loudspeaker):
    producer_name = str(loudspeaker.producer.name)
    return producer_name

def get_type_name(loudspeaker):
    type_name = str(loudspeaker.type.name)
    return type_name

class LoudspeakerView(View):
    def get(self, request):
        print("Getting all loudspeakers")
        start = int(request.GET.get('_start', 0))
        limit = int(request.GET.get('_limit', 12))
        loudspeakers = LoudSpeaker.objects.filter(is_active=True)
        check = check_data_exists(loudspeakers)
        if check[0] is False:
            return JsonResponse(check[1])
        total = len(loudspeakers)
        data = []
        for loudspeaker in loudspeakers[start:start + limit]:
            loudspeaker_serializer = LoudspeakerSerializer(loudspeaker).data
            loudspeaker_serializer["producer"] = get_producer_name(loudspeaker)
            loudspeaker_serializer["type"] = get_type_name(loudspeaker)
            data.append(loudspeaker_serializer)

        return JsonResponse({
                'status': 'Success',
                'status_code': status.HTTP_200_OK,
                'message': 'Data retrieved successfully',
                'data': {
                    'total': total,
                    'loudspeakers': data
                }
            })
        

    def post(self, request):
        serializer = LoudspeakerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoudspeakerDetailView(View):
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
            'status_code': status.HTTP_200_OK,
            'message': 'Data retrieved successfully',
            'data': loudspeaker_serializer
        })

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

class LoudspeakerSearchByProducerView(View):
    def get(self, request):
        print("Looking for loudspeakers by producer")
        query = request.GET.get('_query', "all")
        start = int(request.GET.get('_start', 0))
        limit = int(request.GET.get('_limit', 12))
        if query == "all":
            loudspeakers = LoudSpeaker.objects.filter(is_active=True).order_by('-created_at')[start:start+limit]
        else:
            loudspeakers = LoudSpeaker.objects.filter(name__icontains=query, is_active=True).order_by('-created_at')[start:start+limit]
        check = check_data_exists(loudspeakers)
        if check[0] is False:
            return JsonResponse(check[1])
        data = []
        for loudspeaker in loudspeakers:
            loudspeaker_serializer = LoudspeakerSerializer(loudspeaker).data
            loudspeaker_serializer["producer"] = get_producer_name(loudspeaker)
            loudspeaker_serializer["type"] = get_type_name(loudspeaker)
            data.append(loudspeaker_serializer)

        return JsonResponse({
                'status': 'Success',
                'status_code': status.HTTP_200_OK,
                'message': 'Data retrieved successfully',
                'data': data
            })
        
    def post(self, request):
        pass
        
class LoudspeakerSearchByNameView(View):
    def get(self, request):
        print('Looking for loudspeakers by name')
        query = str(request.GET.get('_query', "all"))
        start = int(request.GET.get('_start', 0))
        limit = int(request.GET.get('_limit', 12))
        if query == "all":
            loudspeakers = LoudSpeaker.objects.filter(is_active=True).order_by('-created_at')
        else:
            loudspeakers = LoudSpeaker.objects.filter(name__icontains=query, is_active=True).order_by('-created_at')
        check = check_data_exists(loudspeakers)
        if check[0] is False:
            return JsonResponse(check[1])
        data = []
        for loudspeaker in loudspeakers:
            loudspeaker_serializer = LoudspeakerSerializer(loudspeaker).data
            loudspeaker_serializer["producer"] = get_producer_name(loudspeaker)
            loudspeaker_serializer["type"] = get_type_name(loudspeaker)
            data.append(loudspeaker_serializer)

        return JsonResponse({
                'status': 'Success',
                'status_code': status.HTTP_200_OK,
                'message': 'Data retrieved successfully',
                'data': data
            })
        
    def post(self, request):
        pass
  
class LoudspeakerFilterView(View):
    def get(self, request):
        print("Filtering loudspeakers")
        producer = request.GET.get('_producer', "all")
        type_loudspeaker = request.GET.get('_type', "all")
        price = request.GET.get('_price', "all")
        if "-" in price:
            price_range = price.split("-")
        start = int(request.GET.get('_start', 0))
        limit = int(request.GET.get('_limit', 12))
        print(producer, type_loudspeaker, price)
        if producer != "all" and type_loudspeaker != "all" and price != "all":
            loudspeakers = LoudSpeaker.objects.filter(producer__slug=producer, type__slug=type_loudspeaker, price__gte=price_range[0], price__lte=price_range[1], is_active=True).order_by('-created_at')[start:start+limit]
        elif producer != "all" and type_loudspeaker != "all":
            loudspeakers = LoudSpeaker.objects.filter(producer__slug=producer, type__slug=type_loudspeaker, is_active=True).order_by('-created_at')[start:start+limit]
        elif producer != "all" and price != "all":
            loudspeakers = LoudSpeaker.objects.filter(producer__slug=producer, price__gte=price_range[0], price__lte=price_range[1], is_active=True).order_by('-created_at')[start:start+limit]
        elif type_loudspeaker != "all" and price != "all":
            loudspeakers = LoudSpeaker.objects.filter(type__slug=type_loudspeaker, price__gte=price_range[0], price__lte=price_range[1], is_active=True).order_by('-created_at')[start:start+limit]
        elif producer != "all":
            loudspeakers = LoudSpeaker.objects.filter(producer__slug=producer, is_active=True).order_by('-created_at')[start:start+limit]
        elif type_loudspeaker != "all":
            loudspeakers = LoudSpeaker.objects.filter(type__slug=type_loudspeaker, is_active=True).order_by('-created_at')[start:start+limit]
        elif price != "all":
            loudspeakers = LoudSpeaker.objects.filter(price__gte=price_range[0], price__lte=price_range[1], is_active=True).order_by('-created_at')[start:start+limit]
        else:
            loudspeakers = LoudSpeaker.objects.filter(is_active=True).order_by('-created_at')[start:start+limit]
        check = check_data_exists(loudspeakers)
        if check[0] is False:
            return JsonResponse(check[1])
        total = len(loudspeakers)
        data = []
        for loudspeaker in loudspeakers:
            loudspeaker_serializer = LoudspeakerSerializer(loudspeaker).data
            loudspeaker_serializer["producer"] = get_producer_name(loudspeaker)
            loudspeaker_serializer["type"] = get_type_name(loudspeaker)
            data.append(loudspeaker_serializer)

        return JsonResponse({
                'status': 'Success',
                'status_code': status.HTTP_200_OK,
                'message': 'Data retrieved successfully',
                'data': {
                    'total': total,
                    'loudspeakers': data
                }
            })
        
    def post(self, request):
        pass
