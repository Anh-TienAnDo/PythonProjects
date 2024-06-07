from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *

# Create your views here.
# get list, post
class ClothesListCreateView(generics.ListCreateAPIView):
    queryset = Clothes.objects.all()
    serializer_class = ClothesSerializer

# get, put, delete by id
class ClothesRetrieveUpdateDestroyAPIViewID(generics.RetrieveUpdateDestroyAPIView):
    queryset = Clothes.objects.all()
    serializer_class = ClothesSerializer
    lookup_field = "id"

# get, put, delete by slug
class ClothesRetrieveUpdateDestroyAPIViewSLUG(generics.RetrieveUpdateDestroyAPIView):
    queryset = Clothes.objects.all()
    serializer_class = ClothesSerializer
    lookup_field = "slug"


# class ClothesDetailId(generics.RetrieveAPIView):
#     def get(self, request, id):
#         queryset = Clothes.objects.get(id=id)
#         serializer_class = ClothesSerializer(queryset).data
#         return Response(serializer_class)
#
# class ClothesDetailSlug(generics.RetrieveAPIView):
#     def get(self, request, slug):
#         queryset = Clothes.objects.get(slug=slug)
#         serializer_class = ClothesSerializer(queryset).data
#         return Response(serializer_class)

class ProducerListCreateView(generics.ListCreateAPIView):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer

class ProducerDetailView(generics.RetrieveAPIView):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer

class TypeListCreateView(generics.ListCreateAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

class TypeDetailView(generics.RetrieveAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
