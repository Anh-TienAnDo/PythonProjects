from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.generic import View
from media_social.service import *
from ThuVien3Goc.settings import ITEMS_PER_PAGE
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_all_by_type(request, type_media):
    service = MediaSocialFilterService(request=request)
    author_name = str(request.GET.get('author_name', ''))
    category_name = str(request.GET.get('category_name', ''))
    producer_name = str(request.GET.get('producer_name', ''))
    time_total = str(request.GET.get('time_total', 0))
    
    page = request.GET.get('page', 1)
    items_per_page = ITEMS_PER_PAGE
    start = (int(page) - 1) * int(items_per_page)
    limit = int(items_per_page)
    
    media_socials = dict(service.filter(type_media=type_media, start=start, limit=limit))
    
    total_items = media_socials.get('total_items', 0)
    media_socials = media_socials.get('data', [])
    
    content = {
        'media_socials': media_socials,
        'page_title': 'Danh sách media social',
        
        'page': page,
        'items_per_page': items_per_page,
        'total_items': total_items,
        'type_media': type_media,
        'author_name': author_name,
        'category_name': category_name,
        'producer_name': producer_name,
        'time_total': time_total
    }
    # return JsonResponse(data=content)
    return render(request, 'media/index.html', content)

def get_detail(request, type_media, slug):
    service = MediaSocialService(request=request)
    media_social = service.get_detail(type_media=type_media, slug=slug)
    media_social = media_social.get('data', None)
    content = {
        'media_social': media_social,
        'page_title': 'Chi tiết media social'
    }
    return JsonResponse(data=content)
    # return render(request, 'media_social/detail.html', content)

def search_and_filter(request):
    service = MediaSocialSearchAndFilterService(request=request)
    
    query = str(request.GET.get('query', ''))
    author_name = str(request.GET.get('author_name', ''))
    category_name = str(request.GET.get('category_name', ''))
    producer_name = str(request.GET.get('producer_name', ''))
    type_media = str(request.GET.get('type_media', ''))
    time_total = str(request.GET.get('time_total', 0))

    page = request.GET.get('page', 1)
    items_per_page = ITEMS_PER_PAGE
    start = (int(page) - 1) * int(items_per_page)
    limit = int(items_per_page)

    media_socials = service.search_and_filter(start=start, limit=limit)

    total_items = media_socials.get('total_items', 0)
    media_socials = media_socials.get('data', [])

    content = {
        'media_socials': media_socials,
        'page_title': 'Tìm kiếm media social',

        'page': page,
        'items_per_page': items_per_page,
        'total_items': total_items,
        
        'query': query,
        'author_name': author_name,
        'category_name': category_name,
        'producer_name': producer_name,
        'type_media': type_media,
        'time_total': time_total
        
    }
    # return JsonResponse(data=content)
    return render(request, 'media/search.html', content)
