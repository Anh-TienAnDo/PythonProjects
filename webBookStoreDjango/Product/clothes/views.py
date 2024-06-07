from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from . import clothes as service

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

class ShowAllClothesByType(APIView):
    def get(self, request, id):
        clothes = Clothes.objects.filter(type_id__id=id)
        clothes = ClothesSerializer(clothes, many=True).data
        return Response(clothes)

class ClothesSearchAPIView(APIView):
    def get(self, request):
        query = str(request.GET.get('query')).lower()
        print(query)
        search_results = service.search_clothes(query)
        clothes = ClothesSerializer(search_results, many=True).data
        return Response(clothes)
