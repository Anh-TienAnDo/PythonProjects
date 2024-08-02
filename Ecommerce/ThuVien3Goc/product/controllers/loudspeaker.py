from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from product.services.loudspeaker import *

class LoudSpeakerView(View):
    def get(self, request):
        loudspeakers_filter_service = LoudspeakerFilterService(request)
        producer = request.GET.get('producer', 'all')
        type_loudspeaker = request.GET.get('type', 'all')
        price = request.GET.get('price', 'all')
        loudspeakers = dict(loudspeakers_filter_service.filter(producer=producer, type_loudspeaker=type_loudspeaker, price=price, start=0, limit=12))
        loudspeakers = loudspeakers.get('loudspeakers', [])
        content = {
            'loudspeakers': loudspeakers,
            'page_title': 'Loa nghe nhạc'
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
        query = str(request.GET.get('query')).lower()
        loudspeaker_search_service = LoudspeakerSearchService(request)
        loudspeaker_by_producer = loudspeaker_search_service.search_loudspeaker_by_producer(query=query, start=0, limit=12)
        loudspeaker_by_name = loudspeaker_search_service.search_loudspeaker_by_name(query=query, start=0, limit=12)
        if loudspeaker_by_producer is None:
            loudspeaker_by_producer = []
        if loudspeaker_by_name is None:
            loudspeaker_by_name = []
        loudspeakers = loudspeaker_by_producer + loudspeaker_by_name
        content = {
            'loudspeakers': loudspeakers,
            'page_title': 'Tìm kiếm loa nghe nhạc'
        }
        return render(request, 'product/loudspeaker/search.html', content)
    
    def post(self, request):
        pass