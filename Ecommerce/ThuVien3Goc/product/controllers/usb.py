from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from product.services.usb import *


class USBView(View):
    def get(self, request):
        usb_filter_service = USBFilterService(request)
        producer = request.GET.get('producer', 'all')
        type_usb = request.GET.get('type', 'all')
        price = request.GET.get('price', 'all')
        usbs = dict(usb_filter_service.filter(producer=producer, type_usb=type_usb, price=price, start=0, limit=12))
        usbs = usbs.get('usbs', [])
        content = {
            'usbs': usbs,
            'page_title': 'USB'
        }
        return render(request, 'product/usb/index.html', content)
    
    def post(self, request):
        pass
    
class USBDetailView(View):
    def get(self, request, slug):
        usb_service = USBService(request)
        usb = usb_service.get_usb_by_slug(slug)
        content = {
            'usb': usb,
            'page_title': 'Chi tiết USB'
        }
        return render(request, 'product/usb/detail.html', content)

    def put(self, request, id):
        pass
    
    def delete(self, request, id):
        pass
    
class USBSearchView(View):
    def get(self, request):
        query = str(request.GET.get('_query')).lower()
        usb_search_service = USBSearchService(request)
        usbs_by_producer = usb_search_service.search_usb_by_producer(query, start=0, limit=12)
        usbs_by_name = usb_search_service.search_usb_by_name(query, start=0, limit=12)
        if usbs_by_producer is None:
            usbs_by_producer = []
        if usbs_by_name is None:
            usbs_by_name = []
        usbs = usbs_by_producer + usbs_by_name
        content = {
            'usbs': usbs,
            'page_title': 'Tìm kiếm USB'
        }
        return render(request, 'product/usb/search.html', content)
    
    def post(self, request):
        pass