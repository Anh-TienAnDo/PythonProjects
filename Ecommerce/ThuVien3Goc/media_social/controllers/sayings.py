from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from media_social.services.sayings import *
from ThuVien3Goc.settings import ITEMS_PER_PAGE
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SayingsView(View):
    def get(self, request):
        sayings_filter_service = SayingsFilter(request=request)
        author_slug = str(request.GET.get('author_slug', 'all'))
        category_slug = str(request.GET.get('category_slug', 'all'))
        
        page = request.GET.get('page', 1)
        items_per_page = ITEMS_PER_PAGE
        start = (int(page) - 1) * int(items_per_page)
        limit = int(items_per_page)
        sayings = dict(sayings_filter_service.filter(author_slug=author_slug, category_slug=category_slug, start=start, limit=limit))
        
        total_items = sayings.get('total', 0)
        sayings = sayings.get('sayings', [])
        
        content = {
            'sayings': sayings,
            'page_title': 'Danh sách câu nói',
            
            'page': page,
            'items_per_page': items_per_page,
            'total_items': total_items,
            'author_slug': author_slug,
            'category_slug': category_slug,
        }
        return render(request, 'media/sayings/index.html', content)
    
    def post(self, request):
        pass
    
class SayingsDetailView(View):
    def get(self, request, slug):
        sayings_service = ServiceSayings(request=request)
        saying = sayings_service.get_sayings_by_slug(slug)
        content = {
            'saying': saying,
            'page_title': 'Chi tiết câu nói'
        }
        return render(request, 'media/sayings/detail.html', content)

    def put(self, request, id):
        pass
    
    def delete(self, request, id):
        pass
    
class SayingsSearchView(View):
    def get(self, request):
        query = str(request.GET.get('query'))
        sayings_search_service = SayingsSearchService(request=request)
        sayings_by_title = sayings_search_service.search_by_title(query=query, start=0, limit=12)
        sayings_by_content = sayings_search_service.search_by_content(query=query, start=0, limit=12)
        
        if sayings_by_title is None:
            sayings_by_title = []
        if sayings_by_content is None:
            sayings_by_content = []
        
        sayings = sayings_by_title + sayings_by_content
        page_title = 'Kết quả tìm kiếm'
        return render(request, 'media/sayings/search.html', {'sayings': sayings, 'page_title': page_title, 'query': query})
    
    def post(self, request):
        pass
