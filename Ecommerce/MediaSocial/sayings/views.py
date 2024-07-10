from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Saying
from .serializers import SayingSerializer
from category.serializers import CategorySerializer
from author.serializers import AuthorSerializer

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

def get_author_name(saying):
    author_name = str(saying.author.name)
    return author_name

def get_category_data(saying):
    categories = saying.categories.all()
    category_data = CategorySerializer(categories, many=True).data
    return category_data

def count_sayings(request):
    sayings_count = Saying.objects.filter(is_active=True).count()
    return Response({
                'status': 'Success',
                'status_code': status.HTTP_200_OK,
                'message': 'Data retrieved successfully',
                'data': sayings_count
            })


class SayingView(APIView):
    def get(self, request):
        start = int(request.query_params.get('start', 0))
        sayings = Saying.objects.filter(is_active=True).order_by('-created_at')[start:start+12]
        check = check_data_exists(sayings)
        if check[0] is False:
            return Response(check[1])
        data = []
        for saying in sayings:
            saying_data = SayingSerializer(saying).data  # Get saying data
            saying_data['categories'] = get_category_data(saying)  # Add categories to the saying data
            saying_data['author'] = get_author_name(saying)  # Add author to the saying data
            data.append(saying_data)  # Add the saying with categories to the data list
        return Response({
                'status': 'Success',
                'status_code': status.HTTP_200_OK,
                'message': 'Data retrieved successfully',
                'data': data
            })

    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)
        serializer = SayingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SayingDetailView(APIView):
    def get(self, request, slug):
        saying = Saying.objects.filter(slug=slug, is_active=True).first()
        check = check_data_exists(saying)
        if check[0] is False:
            return Response(check[1])
        saying_data = SayingSerializer(saying).data  # Get saying data
        saying.view += 1  # Increase the view count by 1
        saying.save()  # Save the view count    
        saying_data['categories'] = get_category_data(saying)  # Add categories to the saying data
        saying_data['author'] = get_author_name(saying)  # Add author to the saying data
        return Response({
                'status': 'Success',
                'status_code': status.HTTP_200_OK,
                'message': 'Data retrieved successfully',
                'data': saying_data
            })
    
    def put(self, request, slug):
        try:
            saying = Saying.objects.get(slug=slug)
        except Saying.DoesNotExist:
            return Response({
                'status': 'Failed',
                'status_code': status.HTTP_404_NOT_FOUND,
                'message': 'Saying not found',
                'data': None
            })
        serializer = SayingSerializer(instance=saying, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        try:
            saying = Saying.objects.get(slug=slug)
        except Saying.DoesNotExist:
            return Response({
                'status': 'Failed',
                'status_code': status.HTTP_404_NOT_FOUND,
                'message': 'Saying not found',
                'data': None
            })
        saying.is_active = False
        saying.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class SayingByCategoryView(APIView):
    def get(self, request, category_slug):
        start = int(request.query_params.get('start', 0))
        sayings = Saying.objects.filter(categories__slug=category_slug, is_active=True).order_by('-created_at')[start:start+12]
        check = check_data_exists(sayings)
        if check[0] is False:
            return Response(check[1])
        data = []
        for saying in sayings:
            saying_data = SayingSerializer(saying).data  # Get saying data
            saying_data['categories'] = get_category_data(saying)  # Add categories to the saying data
            saying_data['author'] = get_author_name(saying)  # Add author to the saying data
            data.append(saying_data)  # Add the saying with categories to the data list
        return Response({
                'status': 'Success',
                'status_code': status.HTTP_200_OK,
                'message': 'Data retrieved successfully',
                'data': data
            })
    
class SayingByAuthorView(APIView):
    def get(self, request, author_slug):
        start = int(request.query_params.get('start', 0))
        sayings = Saying.objects.filter(author__slug=author_slug, is_active=True).order_by('-created_at')[start:start+12]
        check = check_data_exists(sayings)
        if check[0] is False:
            return Response(check[1])
        data = []
        for saying in sayings:
            saying_data = SayingSerializer(saying).data  # Get saying data
            saying_data['categories'] = get_category_data(saying)  # Add categories to the saying data
            saying_data['author'] = get_author_name(saying)  # Add author to the saying data
            data.append(saying_data)  # Add the saying with categories to the data list
        
        return Response({
                'status': 'Success',
                'status_code': status.HTTP_200_OK,
                'message': 'Data retrieved successfully',
                'data': data
            })
    
class SayingByCategoryAndAuthorView(APIView):
    def get(self, request, category_slug, author_slug):
        start = int(request.query_params.get('start', 0))
        sayings = Saying.objects.filter(categories__slug=category_slug, author__slug=author_slug, is_active=True).order_by('-created_at')[start:start+12] 
        check = check_data_exists(sayings)
        if check[0] is False:
            return Response(check[1])   
        data = []
        for saying in sayings:
            saying_data = SayingSerializer(saying).data  # Get saying data
            saying_data['categories'] = get_category_data(saying)  # Add categories to the saying data
            saying_data['author'] = get_author_name(saying)  # Add author to the saying data
            data.append(saying_data)  # Add the saying with categories to the data list
        return Response({
                'status': 'Success',
                'status_code': status.HTTP_200_OK,
                'message': 'Data retrieved successfully',
                'data': data
            })
