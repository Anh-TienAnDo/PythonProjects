from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from media_social.services.sayings import *
from product.services.loudspeaker import *
from product.services.memory_stick import *
from product.services.usb import *
import json
from django_ratelimit.decorators import ratelimit
# from django.utils.decorators import method_decorator
# class MyView(View):
#     @method_decorator(ratelimit(key='ip', rate='1/m', method='GET'))
#     def get(self, request):
#         pass

# Create your views here.
@ratelimit(key='ip', rate='10/m', method='GET', block=False)
def index(request):
    sayings_filter_service = SayingsFilter(request=request)
    author_slug = str(request.GET.get('author_slug', 'all'))
    category_slug = str(request.GET.get('category_slug', 'all'))
    start = 0
    limit = 12
    
    sayings = sayings_filter_service.filter(author_slug=author_slug, category_slug=category_slug, start=start, limit=limit)
    total_items = sayings.get('total', 0)
    sayings = sayings.get('sayings', [])
    content = {
        'sayings': sayings,
        'page_title': 'Trang chủ',
        'total_items': total_items,
        'author_slug': author_slug,
        'category_slug': category_slug,
        'meta': json.dumps(request.META)
    }
    return render(request, 'core/index.html', content)

def search(request):
    query = str(request.GET.get('query'))
    sayings_search_service = SayingsSearchService(request=request)
    sayings_by_title = sayings_search_service.search_by_title(query, start=0, limit=3)
    sayings_by_content = sayings_search_service.search_by_content(query, start=0, limit=3)
    sayings_by_author = sayings_search_service.search_by_author(query, start=0, limit=3)
    if sayings_by_title is None:
        sayings_by_title = []
    if sayings_by_content is None:
        sayings_by_content = []
    if sayings_by_author is None:
        sayings_by_author = []
    sayings = sayings_by_title + sayings_by_content + sayings_by_author
    
    loudspeaker_search_service = LoudspeakerSearchService(request=request)
    loudspeaker_by_producer = loudspeaker_search_service.search_loudspeaker_by_producer(query=query, start=0, limit=3)
    loudspeaker_by_name = loudspeaker_search_service.search_loudspeaker_by_name(query=query, start=0, limit=3)
    if loudspeaker_by_producer is None:
        loudspeaker_by_producer = []
    if loudspeaker_by_name is None:
        loudspeaker_by_name = []
    loudspeakers = loudspeaker_by_producer + loudspeaker_by_name
    
    memory_stick_search_service = MemoryStickSearchService(request=request)
    memory_stick_by_producer = memory_stick_search_service.search_memory_stick_by_producer(query=query, start=0, limit=3)
    memory_stick_by_name = memory_stick_search_service.search_memory_stick_by_name(query=query, start=0, limit=3)
    if memory_stick_by_producer is None:
        memory_stick_by_producer = []
    if memory_stick_by_name is None:
        memory_stick_by_name = []
    memory_sticks = memory_stick_by_name + memory_stick_by_producer
    
    usb_search_service = USBSearchService(request=request)
    usbs_by_producer = usb_search_service.search_usb_by_producer(query, start=0, limit=3)
    usbs_by_name = usb_search_service.search_usb_by_name(query, start=0, limit=3)
    if usbs_by_producer is None:
        usbs_by_producer = []
    if usbs_by_name is None:
        usbs_by_name = []
    usbs = usbs_by_producer + usbs_by_name
    content = {
        'usbs': usbs,
        'sayings': sayings,
        'loudspeakers': loudspeakers,
        'memory_sticks': memory_sticks,
        'page_title': 'Tìm kiếm'
    }
    return render(request, 'core/search.html', content)
    
    
