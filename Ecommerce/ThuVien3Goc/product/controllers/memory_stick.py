from django.http import HttpResponse
from django. shortcuts import render, redirect
from django.views.generic import View
from product.services.memory_stick import *

class MemoryStickView(View):
    def get(self, request):
        memory_stick_service = MemoryStickService()
        memory_sticks_data = memory_stick_service.get_all_memory_stick(start=0, limit=12)
        memory_sticks = memory_sticks_data.get('memory_sticks')
        content = {
            'memory_sticks': memory_sticks,
            'page_title': 'Memory Stick'
        }
        return render(request, 'product/memory_stick/index.html', content)
    
    def post(self, request):
        pass
    
class MemoryStickDetailView(View):
    def get(self, request, slug):
        memory_stick_service = MemoryStickService()
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
        memory_stick_service = MemoryStickService()
        memory_sticks = memory_stick_service.get_all_memory_stick(start=0, limit=12)
        content = {
            'memory_sticks': memory_sticks,
            'page_title': 'Tìm kiếm Memory Stick'
        }
        return render(request, 'product/memory_stick/search.html', content)
    
    def post(self, request):
        pass