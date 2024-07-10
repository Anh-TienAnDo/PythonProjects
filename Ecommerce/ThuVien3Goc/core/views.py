from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from media_social.service import ServiceSayings, SayingsFilter

# Create your views here.
def index(request):
    content = {}
    content['sayings'] = SayingsFilter(request).filter_sayings()
    page_title = 'Trang chủ'
    return render(request, 'core/index.html', {'content': content, 'page_title': page_title})
