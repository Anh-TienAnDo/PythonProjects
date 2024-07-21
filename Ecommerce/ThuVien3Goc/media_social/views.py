from django.shortcuts import render
from django.http import HttpResponse
from .service import ServiceSayings, SayingsFilter

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


