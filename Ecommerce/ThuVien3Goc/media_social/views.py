from django.shortcuts import render
from django.http import HttpResponse
from .service import ServiceSayings, SayingsFilter, SayingsSearchService

# Create your views here.
def get_sayings(request):
    saying_filter_service = SayingsFilter(request)
    sayings = saying_filter_service.filter_sayings()
    page_title = 'sayings'
    return render(request, 'media/sayings/index.html', {'sayings': sayings, 'page_title': page_title})

def get_detail_saying(request, slug):
    saying_service = ServiceSayings()
    saying = saying_service.get_detail_sayings(slug)
    page_title = 'detail_saying'
    return render(request, 'media/sayings/detail.html', {'saying': saying, 'page_title': page_title})

def search_sayings(request):
    query = request.GET.get('query')
    saying_search_service = SayingsSearchService()
    sayings_by_title = saying_search_service.search_by_title(query)
    sayings_by_author = saying_search_service.search_by_author(query)
    sayings_by_content = saying_search_service.search_by_content(query)
    if sayings_by_title is None:
        sayings_by_title = []
    if sayings_by_content is None:
        sayings_by_content = []
    if sayings_by_author is None:
        sayings_by_author = []
    sayings = sayings_by_title + sayings_by_author + sayings_by_content
    page_title = 'search_sayings'
    return render(request, 'media/sayings/search.html', {'sayings': sayings, 'page_title': page_title})

