from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from media_social.service import *
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
    service = MediaSocialFilterService(request=request)
    author_name = str(request.GET.get('author_name', ''))
    category_name = str(request.GET.get('category_name', ''))
    start = 0
    limit = 12
    
    media_socials = dict(service.filter(type_media="", start=start, limit=limit))
    
    total_items = media_socials.get('total_items', 0)
    media_socials = media_socials.get('data', [])
    
    content = {
        'media_socials': media_socials,
        'page_title': 'Trang chủ',
        
        'total_items': total_items,
        'author_name': author_name,
        'category_name': category_name,
    }
    return render(request, 'core/index.html', content)

def search(request):
    query = str(request.GET.get('query'))
    service = MediaSocialSearchAndFilterService(request=request)
    media_socials = service.search_and_filter(start=0, limit=12)
    media_socials = media_socials.get('data', [])
    
    loudspeaker_search_service = LoudspeakerSearchService(request=request)
    loudspeakers = loudspeaker_search_service.search_and_filter(query=query, start=0, limit=3).get('loudspeakers', [])
    
    memory_stick_search_service = MemoryStickSearchService(request=request)
    memory_sticks = memory_stick_search_service.search_and_filter(query=query, start=0, limit=12).get('memory_sticks', [])
    
    usb_search_service = USBSearchService(request=request)
    usbs = usb_search_service.search_and_filter(query=query, start=0, limit=3).get('usbs', [])
    content = {
        'usbs': usbs,
        'media_socials': media_socials,
        'loudspeakers': loudspeakers,
        'memory_sticks': memory_sticks,
        'page_title': 'Tìm kiếm'
    }
    # return HttpResponse(json.dumps(content))
    return render(request, 'core/search.html', content)
    
    
