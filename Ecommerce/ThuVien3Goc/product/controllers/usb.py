from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from product.services.usb import *
from ThuVien3Goc.settings import ITEMS_PER_PAGE


class USBView(View):
    def get(self, request):
        usb_filter_service = USBFilterService(request)
        producer = str(request.GET.get('producer', ''))
        type_usb = str(request.GET.get('type', ''))
        price = int(request.GET.get('price', 0))
        
        page = request.GET.get('page', 1)
        # items_per_page = request.GET.get('items_per_page', ITEMS_PER_PAGE)
        items_per_page = ITEMS_PER_PAGE
        start = (int(page) - 1) * int(items_per_page)
        limit = int(items_per_page)
        usbs = usb_filter_service.filter(producer=producer, type_usb=type_usb, price=price, start=start, limit=limit)
        
        total_items = usbs.get('total', 0)
        usbs = usbs.get('usbs', [])
        content = {
            'usbs': usbs,
            'page_title': 'USB',
            
            'page': page,
            'items_per_page': items_per_page,
            'total_items': total_items,
            'producer': producer,
            'type': type_usb,
            'price': price,
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
        usb_search_service = USBSearchService(request)
        query = str(request.GET.get('query'))
        producer = str(request.GET.get('producer', ''))
        type_usb = str(request.GET.get('type', ''))
        price = int(request.GET.get('price', 0))
        
        page = request.GET.get('page', 1)
        # items_per_page = request.GET.get('items_per_page', ITEMS_PER_PAGE)
        items_per_page = ITEMS_PER_PAGE
        start = (int(page) - 1) * int(items_per_page)
        limit = int(items_per_page)
        usbs = usb_search_service.search_and_filter(query=query, producer=producer, type_usb=type_usb, price=price, start=start, limit=limit)
        
        total_items = usbs.get('total', 0)
        usbs = usbs.get('usbs', [])
        content = {
            'usbs': usbs,
            'page_title': 'Tìm kiếm USB',
            'query': query if query else '',
            'page': page,
            'items_per_page': items_per_page,
            'total_items': total_items,
            'producer': producer,
            'type': type_usb,
            'price': price,
        }
        return render(request, 'product/usb/search.html', content)
    
    def post(self, request):
        pass