from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from product.services.usb import *


class USBView(View):
    def get(self, request):
        usb_service = USBService()
        usbs_data = usb_service.get_all_usb(start=0, limit=12)
        usbs = usbs_data.get('usbs')
        content = {
            'usbs': usbs,
            'page_title': 'USB'
        }
        return render(request, 'product/usb/index.html', content)
    
    def post(self, request):
        pass
    
class USBDetailView(View):
    def get(self, request, slug):
        usb_service = USBService()
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
        usb_service = USBService()
        usbs = usb_service.get_all_usb(start=0, limit=12)
        content = {
            'usbs': usbs,
            'page_title': 'Tìm kiếm USB'
        }
        return render(request, 'product/usb/search.html', content)
    
    def post(self, request):
        pass