from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from product.services.loudspeaker import *
from product.services.memory_stick import *
from product.services.usb import *
import json
# from django_ratelimit.decorators import ratelimit
# from django.utils.decorators import method_decorator
# class MyView(View):
#     @method_decorator(ratelimit(key='ip', rate='1/m', method='GET'))
#     def get(self, request):
#         pass

# Create your views here.
# @ratelimit(key='ip', rate='10/m', method='GET', block=False)
def index(request):
    content = {
        'page_title': 'Trang chủ'
    }
    return render(request, 'core/index.html', content)

def search(request):
    query = str(request.GET.get('query'))
    
    loudspeaker_search_service = LoudspeakerSearchService(request=request)
    loudspeakers = dict(loudspeaker_search_service.search_and_filter(query=query)).get('loudspeakers', [])
    
    memory_stick_search_service = MemoryStickSearchService(request=request)
    memory_sticks = dict(memory_stick_search_service.search_and_filter(query=query)).get('memory_sticks', [])
    
    usb_search_service = USBSearchService(request=request)
    usbs = dict(usb_search_service.search_and_filter(query=query)).get('usbs', [])
    content = {
        'usbs': usbs,
        'loudspeakers': loudspeakers,
        'memory_sticks': memory_sticks,
        'page_title': 'Tìm kiếm'
    }
    # return HttpResponse(json.dumps(content))
    return render(request, 'core/search.html', content)
    
    
