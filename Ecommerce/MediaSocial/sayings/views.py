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


class SayingView(APIView):
    def get(self, request):
        print("GET SAYINGS")
        start = int(request.GET.get('_start', 0))
        limit = int(request.GET.get('_limit', 12))
        sayings = Saying.objects.filter(is_active=True).order_by('-created_at')
        check = check_data_exists(sayings)
        if check[0] is False:
            return Response(check[1])
        total = sayings.count()
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
                'data': {
                    'total': total,
                    'sayings': data
                }
            })

    # @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)
        serializer = SayingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SayingDetailView(APIView):
    def get(self, request, slug):
        print("GET SAYING DETAIL")
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

class SayingFilterView(APIView):
    def get(self, request):
        start = int(request.GET.get('_start', 0))
        limit = int(request.GET.get('_limit', 12))
        author_slug = str(request.GET.get('_author_slug', 'all'))
        category_slug = str(request.GET.get('_category_slug', 'all'))
        if author_slug != 'all' and category_slug != 'all':
            sayings = Saying.objects.filter(author__slug=author_slug, categories__slug=category_slug, is_active=True).order_by('-created_at')
        elif author_slug != 'all':
            sayings = Saying.objects.filter(author__slug=author_slug, is_active=True).order_by('-created_at')
        elif category_slug != 'all':
            sayings = Saying.objects.filter(categories__slug=category_slug, is_active=True).order_by('-created_at')
        else:
            sayings = Saying.objects.filter(is_active=True).order_by('-created_at')
        check = check_data_exists(sayings)
        if check[0] is False:
            return Response(check[1])
        total = sayings.count()
        sayings = sayings[start:start+limit]
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
                'data': {
                    'total': total,
                    'sayings': data
                }
            })    
          
class SayingSearchByTitleView(APIView):
    def get(self, request):
        start = int(request.GET.get('_start', 0))
        limit = int(request.GET.get('_limit', 12))
        query = str(request.GET.get('_query', ''))
        sayings = Saying.objects.filter(title__icontains=query, is_active=True).order_by('-created_at')[start:start+limit]
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
        
class SayingSearchByContentView(APIView):
    def get(self, request):
        start = int(request.GET.get('_start', 0))
        limit = int(request.GET.get('_limit', 12))
        query = str(request.GET.get('_query', ''))
        sayings = Saying.objects.filter(content__icontains=query, is_active=True).order_by('-created_at')[start:start+limit]
        check = check_data_exists(sayings)
        if check[0] is False:
            return Response(check[1])
        data = []
        for saying in sayings:
            saying_data = SayingSerializer(saying).data
            saying_data['categories'] = get_category_data(saying)
            saying_data['author'] = get_author_name(saying)
            data.append(saying_data)
        return Response({
                'status': 'Success',
                'status_code': status.HTTP_200_OK,
                'message': 'Data retrieved successfully',
                'data': data
            })
        
class SayingSearchByAuthorView(APIView):
    def get(self, request):
        start = int(request.GET.get('_start', 0))
        limit = int(request.GET.get('_limit', 12))
        query = str(request.GET.get('_query', ''))
        sayings = Saying.objects.filter(author__name__icontains=query, is_active=True).order_by('-created_at')[start:start+limit]
        check = check_data_exists(sayings)
        if check[0] is False:
            return Response(check[1])
        data = []
        for saying in sayings:
            saying_data = SayingSerializer(saying).data
            saying_data['categories'] = get_category_data(saying)
            saying_data['author'] = get_author_name(saying)
            data.append(saying_data)
        return Response({
                'status': 'Success',
                'status_code': status.HTTP_200_OK,
                'message': 'Data retrieved successfully',
                'data': data
            })
