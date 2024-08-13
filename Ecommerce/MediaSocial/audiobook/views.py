from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import json
from .serializers import AudioBookSerializer, BookSectionSerializer
from .models import AudioBook, BookSection
from author.serializers import AuthorSerializer
from category.serializers import CategorySerializer
from producer.serializers import ProducerSerializer

# Create your views here.

def get_author_name(audio_book):
    author_name = str(audio_book.author.name)
    return author_name

def get_category_data(audio_book):
    categories = audio_book.categories.all()
    category_data = CategorySerializer(categories, many=True).data
    return category_data

def get_producer_name(audio_book):
    producer_name = str(audio_book.producer.name)
    return producer_name

def get_time(book_section):
    hour = book_section.time // 60
    minute = book_section.time % 60
    return f'{hour}h:{minute}m'

def get_total_time(audio_book):
    hour = audio_book.time_total // 60
    minute = audio_book.time_total % 60
    return f'{hour}h:{minute}m'

class AudioBookView(APIView):
    def get(self, request):
        print("GET AUDIOBOOKS")
        start = int(request.GET.get('_start', 0))
        limit = int(request.GET.get('_limit', 12))
        audio_books = AudioBook.objects.filter(is_active=True).order_by('-created_at')
        data = []
        total = 0
        if audio_books:
            total = audio_books.count()
            for audio_book in audio_books[start:start + limit]:
                audio_book_data = AudioBookSerializer(audio_book).data  # Get audio book data
                audio_book_data['author'] = get_author_name(audio_book)  # Add author to the audio book data
                audio_book_data['categories'] = get_category_data(audio_book)  # Add category to the audio book data
                audio_book_data['producer'] = get_producer_name(audio_book)  # Add producer to the audio book data
                audio_book_data['time_total'] = get_total_time(audio_book)
                data.append(audio_book_data)  # Add the audio book to the data list
                
        return Response({
                'status': 'Success',
                'status_code': status.HTTP_200_OK,
                'message': 'Data retrieved successfully',
                'data': {
                    'total': total,
                    'audio_books': data
                }
            })

    # @csrf_exempt
    def post(self, request):
        print("POST AUDIOBOOK")
        data = request.data
        author = Author.objects.get(id=data['author'])
        category = Category.objects.get(id=data['category'])
        producer = Producer.objects.get(id=data['producer'])
        audio_book = AudioBook(
            title=data['title'],
            author=author,
            category=category,
            producer=producer,
            description=data['description'],
            image=data['image'],
            quantity=data['quantity'],
            time_total=data['time_total']
        )
        audio_book.save()
        return Response({
            'status': 'Success',
            'status_code': status.HTTP_201_CREATED,
            'message': 'Data created successfully',
            'data': AudioBookSerializer(audio_book).data
        })
        
class AudioBookDetailView(APIView):
    def get(self, request, slug):
        print("GET AUDIOBOOK DETAIL")
        audio_book = AudioBook.objects.get(slug=slug)
        audio_book.view += 1
        audio_book.save()
        
        book_sections = BookSection.objects.filter(audio_book=audio_book, is_active=True).order_by('created_at')
        book_sections_data = []
        for book_section in book_sections:
            book_section_data = BookSectionSerializer(book_section).data  # Get book section data
            book_section_data['time'] = get_time(book_section)
            book_sections_data.append(book_section_data)
        
        audio_book_data = AudioBookSerializer(audio_book).data  # Get audio book data
        audio_book_data['author'] = get_author_name(audio_book)
        audio_book_data['categories'] = get_category_data(audio_book)
        audio_book_data['producer'] = get_producer_name(audio_book)
        return Response({
                'status': 'Success',
                'status_code': status.HTTP_200_OK,
                'message': 'Data retrieved successfully',
                'data': {
                    'audio_book': audio_book_data,
                    'book_sections': book_sections_data
                }
            })
    
    def put(self, request, id):
        pass
    
    def delete(self, request, id):
        pass

class AudioBookFilterView(APIView):
    def get(self, request):
        print("GET AUDIOBOOKS FILTER")
        start = int(request.GET.get('_start', 0))
        limit = int(request.GET.get('_limit', 12))
        category = request.GET.get('_category_slug', 'all')
        producer = request.GET.get('_producer_slug', 'all')
        author = request.GET.get('_author_slug', 'all')
        time = request.GET.get('_time', 'all')
        if "-" in time:
            time_range = time.split("-")
        
        if category != 'all' and producer != 'all' and author != 'all' and time != 'all':
            audio_books = AudioBook.objects.filter(categories__slug=category, producer__slug=producer, author__slug=author, time_total__range=(time_range[0], time_range[1]), is_active=True).order_by('-created_at')
        elif category != 'all' and producer != 'all' and author != 'all':
            audio_books = AudioBook.objects.filter(categories__slug=category, producer__slug=producer, author__slug=author, is_active=True).order_by('-created_at')
        elif category != 'all' and producer != 'all' and time != 'all':
            audio_books = AudioBook.objects.filter(categories__slug=category, producer__slug=producer, time_total__range=(time_range[0], time_range[1]), is_active=True).order_by('-created_at')
        elif category != 'all' and author != 'all' and time != 'all':
            audio_books = AudioBook.objects.filter(categories__slug=category, author__slug=author, time_total__range=(time_range[0], time_range[1]), is_active=True).order_by('-created_at')
        elif producer != 'all' and author != 'all' and time != 'all':
            audio_books = AudioBook.objects.filter(producer__slug=producer, author__slug=author, time_total__range=(time_range[0], time_range[1]), is_active=True).order_by('-created_at')
        elif category != 'all' and producer != 'all':
            audio_books = AudioBook.objects.filter(categories__slug=category, producer__slug=producer, is_active=True).order_by('-created_at')
        elif category != 'all' and author != 'all':
            audio_books = AudioBook.objects.filter(categories__slug=category, author__slug=author, is_active=True).order_by('-created_at')
        elif category != 'all' and time != 'all':
            audio_books = AudioBook.objects.filter(categories__slug=category, time_total__range=(time_range[0], time_range[1]), is_active=True).order_by('-created_at')
        elif producer != 'all' and author != 'all':
            audio_books = AudioBook.objects.filter(producer__slug=producer, author__slug=author, is_active=True).order_by('-created_at')
        elif producer != 'all' and time != 'all':
            audio_books = AudioBook.objects.filter(producer__slug=producer, time_total__range=(time_range[0], time_range[1]), is_active=True).order_by('-created_at')
        elif author != 'all' and time != 'all':
            audio_books = AudioBook.objects.filter(author__slug=author, time_total__range=(time_range[0], time_range[1]), is_active=True).order_by('-created_at')
        elif category != 'all':
            audio_books = AudioBook.objects.filter(categories__slug=category, is_active=True).order_by('-created_at')
        elif producer != 'all':
            audio_books = AudioBook.objects.filter(producer__slug=producer, is_active=True).order_by('-created_at')
        elif author != 'all':
            audio_books = AudioBook.objects.filter(author__slug=author, is_active=True).order_by('-created_at')
        elif time != 'all':
            audio_books = AudioBook.objects.filter(time_total__range=(time_range[0], time_range[1]), is_active=True).order_by('-created_at')
        else:
            audio_books = AudioBook.objects.filter(is_active=True).order_by('-created_at')
        
        data = []
        total = 0
        if audio_books:
            total = audio_books.count()
            for audio_book in audio_books[start:start + limit]:
                audio_book_data = AudioBookSerializer(audio_book).data  # Get audio book data
                audio_book_data['author'] = get_author_name(audio_book)  # Add author to the audio book data
                audio_book_data['categories'] = get_category_data(audio_book)  # Add category to the audio book data
                audio_book_data['producer'] = get_producer_name(audio_book)  # Add producer to the audio book data
                audio_book_data['time_total'] = get_total_time(audio_book) # Add total time to the audio book data
                data.append(audio_book_data)  # Add the audio book to the data list
                
        return Response({
                'status': 'Success',
                'status_code': status.HTTP_200_OK,
                'message': 'Data retrieved successfully',
                'data': {
                    'total': total,
                    'audio_books': data
                }
            })
