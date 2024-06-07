from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import *
from .serializers import *
from . import book

# Create your views here.
# get list, post
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# get, put, delete by id
class BookRetrieveUpdateDestroyAPIViewID(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "id"

# get, put, delete by slug
class BookRetrieveUpdateDestroyAPIViewSLUG(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "slug"

# get list, post
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# get, put, delete by id
class CategoryRetrieveUpdateDestroyAPIViewID(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "id"

# get, put, delete by slug
class CategoryRetrieveUpdateDestroyAPIViewSLUG(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"

class ShowAllBookByCategory(APIView):
    def get(self, request, id):
        books = Book.objects.filter(categories__id=id)
        books = BookSerializer(books, many=True).data
        return Response(books)

class BookSearchAPIView(APIView):
    def get(self, request):
        query = str(request.GET.get('query')).lower()
        print(query)
        search_results = book.search_books(query)
        books = BookSerializer(search_results, many=True).data
        return Response(books)

