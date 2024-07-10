from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
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

class LoudspeakerView(APIView):
    def get(self, request):
        start = int(request.GET.get('_start', 0))
        limit = int(request.GET.get('_limit', 12))
        loudspeakers = LoudSpeaker.objects.filter(is_active=True)
        check = check_data_exists(loudspeakers)
        if check[0] is False:
            return Response(check[1])
        total = len(loudspeakers)
        data = []
        for loudspeaker in loudspeakers[start:start + limit]:
            loudspeaker_serializer = LoudspeakerSerializer(loudspeaker).data
            loudspeaker_serializer["producer"] = get_producer_name(loudspeaker)
            loudspeaker_serializer["type"] = get_type_name(loudspeaker)
            data.append(loudspeaker_serializer)

        return Response({
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoudspeakerDetailView(APIView):
    def get(self, request, slug):
        loudspeaker = LoudSpeaker.objects.filter(slug=slug, is_active=True).first()
        check = check_data_exists(loudspeaker)
        if check[0] is False:
            return Response(check[1])
        loudspeaker_serializer = LoudspeakerSerializer(loudspeaker).data
        loudspeaker_serializer["producer"] = get_producer_name(loudspeaker)
        loudspeaker_serializer["type"] = get_type_name(loudspeaker)
        return Response({
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
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        loudspeaker = LoudSpeaker.objects.filter(id=id, is_active=True).first()
        check = check_data_exists(loudspeaker)
        if check[0] is False:
            return Response(check[1])
        loudspeaker.is_active = False
        loudspeaker.save()
        return Response({
            'status': 'Success',
            'status_code': status.HTTP_200_OK,
            'message': 'Data deleted successfully',
            'data': None
        })
