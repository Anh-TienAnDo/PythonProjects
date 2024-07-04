from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Author
from .serializers import AuthorSerializer

# Create your views here.
class AuthorView(APIView):
    def get(self, request):
        authors = Author.objects.filter(is_active=True)
        serializer = AuthorSerializer(authors, many=True)
        return Response({
                'status': 'Success',
                'status_code': status.HTTP_200_OK,
                'message': 'Data retrieved successfully',
                'data': serializer.data
            })

    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)
        serializer = AuthorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
