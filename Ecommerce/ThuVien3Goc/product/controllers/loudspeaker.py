from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from product.services.loudspeaker import *
from ThuVien3Goc.settings import ITEMS_PER_PAGE

class LoudSpeakerView(View):
    def get(self, request):
        loudspeakers_filter_service = LoudspeakerFilterService(request)
        producer = str(request.GET.get('producer', ''))
        type_loudspeaker = str(request.GET.get('type', ''))
        price = int(request.GET.get('price', 0))
        
        page = request.GET.get('page', 1)
        # items_per_page = request.GET.get('items_per_page', ITEMS_PER_PAGE)
        items_per_page = ITEMS_PER_PAGE
        start = (int(page) - 1) * int(items_per_page)
        limit = int(items_per_page)
        loudspeakers = loudspeakers_filter_service.filter(producer=producer, type_loudspeaker=type_loudspeaker, price=price, start=start, limit=limit)
        
        total_items = loudspeakers.get('total', 0)
        loudspeakers = loudspeakers.get('loudspeakers', [])
        
        content = {
            'loudspeakers': loudspeakers,
            'page_title': 'Loa nghe nhạc',
            
            'page': page,
            'items_per_page': items_per_page,
            'total_items': total_items,
            'producer': producer,
            'type': type_loudspeaker,
            'price': price,
        }
        return render(request, 'product/loudspeaker/index.html', content)
    
    def post(self, request):
        pass
    
class LoudSpeakerDetailView(View):
    def get(self, request, slug):
        loudspeaker_service = LoudspeakerService(request)
        loudspeaker = loudspeaker_service.get_loudspeaker_by_slug(slug)
        content = {
            'loudspeaker': loudspeaker,
            'page_title': 'Chi tiết loa nghe nhạc'
        }
        return render(request, 'product/loudspeaker/detail.html', content)

    def put(self, request, id):
        pass
    
    def delete(self, request, id):
        pass
    
class LoudSpeakerSearchView(View):
    def get(self, request):
        loudspeaker_search_service = LoudspeakerSearchService(request)
        
        query = str(request.GET.get('query_loudspeaker', ''))
        producer = str(request.GET.get('producer', ''))
        type_loudspeaker = str(request.GET.get('type', ''))
        price = int(request.GET.get('price', 0))
        
        page = request.GET.get('page', 1)
        items_per_page = ITEMS_PER_PAGE
        start = (int(page) - 1) * int(items_per_page)
        limit = int(items_per_page)
        loudspeakers = loudspeaker_search_service.search_and_filter(query=query, producer=producer, type_loudspeaker=type_loudspeaker, price=price, start=start, limit=limit)
        
        total_items = loudspeakers.get('total', 0)
        loudspeakers = loudspeakers.get('loudspeakers', [])
        
        content = {
            'loudspeakers': loudspeakers,
            'page_title': 'Tìm kiếm loa nghe nhạc',
            'query': query,
            'page': page,
            'items_per_page': items_per_page,
            'total_items': total_items,
            'producer': producer,
            'type': type_loudspeaker,
            'price': price,
        }
    
        return render(request, 'product/loudspeaker/search.html', content)
    
    def post(self, request):
        pass