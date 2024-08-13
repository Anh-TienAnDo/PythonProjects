from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from media_social.services.audio_book import *
from ThuVien3Goc.settings import ITEMS_PER_PAGE
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioBookView(View):
    def get(self, request):
        audio_book_filter_service = AudioBookFilter(request=request)
        author_slug = str(request.GET.get('author_slug', 'all'))
        category_slug = str(request.GET.get('category_slug', 'all'))
        producer_slug = str(request.GET.get('producer_slug', 'all'))
        time = str(request.GET.get('time', 'all'))
        
        page = request.GET.get('page', 1)
        items_per_page = ITEMS_PER_PAGE
        start = (int(page) - 1) * int(items_per_page)
        limit = int(items_per_page)
        audio_books = dict(audio_book_filter_service.filter(author_slug=author_slug, category_slug=category_slug, producer_slug=producer_slug, time=time, start=start, limit=limit))
        
        total_items = audio_books.get('total', 0)
        audio_books = audio_books.get('audio_books', [])
        
        content = {
            'audio_books': audio_books,
            'page_title': 'Danh sách câu nói',
            
            'page': page,
            'items_per_page': items_per_page,
            'total_items': total_items,
            'author_slug': author_slug,
            'category_slug': category_slug,
            'producer_slug': producer_slug,
            'time': time,
        }
        return render(request, 'media/audiobook/index.html', content)
    
    def post(self, request):
        pass
    
class AudioBookDetailView(View):
    def get(self, request, slug):
        audio_book_service = ServiceAudioBook(request=request)
        data = audio_book_service.get_audiobook_by_slug(slug)
        audio_book = data.get('audio_book', None)
        chapters = data.get('book_sections', [])
        content = {
            'audio_book': audio_book,
            'chapters': chapters,
            'page_title': 'Chi tiết câu nói'
        }
        return render(request, 'media/audiobook/detail.html', content)

    def put(self, request, id):
        pass
    
    def delete(self, request, id):
        pass
    
# class AudioBookSearchView(View):
#     def get(self, request):
#         query = str(request.GET.get('query'))
#         AudioBook_search_service = AudioBookSearchService(request=request)
#         AudioBook_by_title = AudioBook_search_service.search_by_title(query=query, start=0, limit=12)
#         AudioBook_by_content = AudioBook_search_service.search_by_content(query=query, start=0, limit=12)
        
#         if AudioBook_by_title is None:
#             AudioBook_by_title = []
#         if AudioBook_by_content is None:
#             AudioBook_by_content = []
        
#         AudioBook = AudioBook_by_title + AudioBook_by_content
#         page_title = 'Kết quả tìm kiếm'
#         return render(request, 'media/AudioBook/search.html', {'AudioBook': AudioBook, 'page_title': page_title, 'query': query})
    
#     def post(self, request):
#         pass
