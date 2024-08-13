from django.http import HttpResponse
from django. shortcuts import render, redirect
from django.views.generic import View
from product.services.memory_stick import *
from ThuVien3Goc.settings import ITEMS_PER_PAGE

class MemoryStickView(View):
    def get(self, request):
        memory_stick_filter_service = MemoryStickFilterService(request)
        producer = request.GET.get('producer', 'all')
        type_memorystick = request.GET.get('type', 'all')
        price = request.GET.get('price', 'all')
        
        page = request.GET.get('page', 1)
        # items_per_page = request.GET.get('items_per_page', ITEMS_PER_PAGE)
        items_per_page = ITEMS_PER_PAGE
        start = (int(page) - 1) * int(items_per_page)
        limit = int(items_per_page)
        memory_sticks = dict(memory_stick_filter_service.filter(producer=producer, type_memorystick=type_memorystick, price=price, start=start, limit=limit))
        
        total_items = memory_sticks.get('total', 0)
        memory_sticks = memory_sticks.get('memory_sticks', [])
        content = {
            'memory_sticks': memory_sticks,
            'page_title': 'Thẻ nhớ',
            
            'page': page,
            'items_per_page': items_per_page,
            'total_items': total_items,
            'producer': producer,
            'type': type_memorystick,
            'price': price,
        }
        return render(request, 'product/memory_stick/index.html', content)
    
    def post(self, request):
        pass
    
class MemoryStickDetailView(View):
    def get(self, request, slug):
        memory_stick_service = MemoryStickService(request)
        memory_stick = memory_stick_service.get_memory_stick_by_slug(slug)
        content = {
            'memory_stick': memory_stick,
            'page_title': 'Chi tiết Memory Stick'
        }
        return render(request, 'product/memory_stick/detail.html', content)

    def put(self, request, id):
        pass
    
    def delete(self, request, id):
        pass
    
class MemoryStickSearchView(View):
    def get(self, request):
        query = str(request.GET.get('_query', ''))
        memory_stick_search_service = MemoryStickSearchService(request)
        memory_stick_by_producer = memory_stick_search_service.search_memory_stick_by_producer(query=query, start=0, limit=12)
        memory_stick_by_name = memory_stick_search_service.search_memory_stick_by_name(query=query, start=0, limit=12)
        if memory_stick_by_producer is None:
            memory_stick_by_producer = []
        if memory_stick_by_name is None:
            memory_stick_by_name = []
        memory_sticks = memory_stick_by_name + memory_stick_by_producer
        content = {
            'memory_sticks': memory_sticks,
            'page_title': 'Tìm kiếm Memory Stick',
            'query': query
        }
        return render(request, 'product/memory_stick/search.html', content)
    
    def post(self, request):
        pass