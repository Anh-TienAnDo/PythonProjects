from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from product.services.loudspeaker import *

class LoudSpeakerView(View):
    def get(self, request):
        loudspeaker_service = LoudspeakerService()
        loudspeakers_data = loudspeaker_service.get_all_loudspeaker(start=0, limit=12)
        loudspeakers = loudspeakers_data.get('loudspeakers')
        content = {
            'loudspeakers': loudspeakers,
            'page_title': 'Loa nghe nhạc'
        }
        return render(request, 'product/loudspeaker/index.html', content)
    
    def post(self, request):
        pass
    
class LoudSpeakerDetailView(View):
    def get(self, request, slug):
        loudspeaker_service = LoudspeakerService()
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
        loudspeaker_service = LoudspeakerService()
        loudspeakers = loudspeaker_service.get_all_loudspeaker(start=0, limit=12)
        content = {
            'loudspeakers': loudspeakers,
            'page_title': 'Tìm kiếm loa nghe nhạc'
        }
        return render(request, 'product/loudspeaker/search.html', content)
    
    def post(self, request):
        pass