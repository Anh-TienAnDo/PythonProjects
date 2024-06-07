from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from . import sevice

# Create your views here.
# get list, post
class PhoneListCreateView(generics.ListCreateAPIView):
    queryset = Phone.objects.all()
    serializer_class = MobileSerializer

# get, put, delete by id
class PhoneRetrieveUpdateDestroyAPIViewID(generics.RetrieveUpdateDestroyAPIView):
    queryset = Phone.objects.all()
    serializer_class = MobileSerializer
    lookup_field = "id"

# get, put, delete by slug
class PhoneRetrieveUpdateDestroyAPIViewSLUG(generics.RetrieveUpdateDestroyAPIView):
    queryset = Phone.objects.all()
    serializer_class = MobileSerializer
    lookup_field = "slug"


class ProducerListCreateView(generics.ListCreateAPIView):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer

# get, put, delete by id
class ProducerRetrieveUpdateDestroyAPIViewID(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
    lookup_field = "id"

# get, put, delete by slug
class ProducerRetrieveUpdateDestroyAPIViewSLUG(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
    lookup_field = "slug"

class TypeListCreateView(generics.ListCreateAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

# get, put, delete by id
class TypeRetrieveUpdateDestroyAPIViewID(generics.RetrieveUpdateDestroyAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    lookup_field = "id"

# get, put, delete by slug
class TypeRetrieveUpdateDestroyAPIViewSLUG(generics.RetrieveUpdateDestroyAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    lookup_field = "slug"

class ShowAllMobilesByType(APIView):
    def get(self, request, id):
        mobiles = Phone.objects.filter(type_id__id=id)
        mobiles = MobileSerializer(mobiles, many=True).data
        return Response(mobiles)

class MobileSearchAPIView(APIView):
    def get(self, request):
        query = str(request.GET.get('query')).lower()
        print(query)
        search_results = sevice.search_mobiles(query)
        mobiles = MobileSerializer(search_results, many=True).data
        return Response(mobiles)
