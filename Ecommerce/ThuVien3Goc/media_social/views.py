from django.shortcuts import render
from django.http import HttpResponse
from .service import ServiceSayings

# Create your views here.
def get_list_sayings(request):
    service = ServiceSayings()
    start = request.query_params.get('start', 0)
    result = service.get_list_sayings(start=start)
    sayings = None
    if result.get('status') == 'Success':
        sayings = result.get('data')
    return render(request, 'sayings/list.html', {'sayings': sayings})

def get_detail_saying(request, id):
    service = ServiceSayings()
    result = service.get_detail_saying(id)
    saying = None
    if result.get('status') == 'Success':
        saying = result.get('data')
    return render(request, 'sayings/detail.html', {'saying': saying})

def get_list_sayings_by_author(request, author_id):
    service = ServiceSayings()
    start = request.query_params.get('start', 0)
    result = service.get_sayings_by_author(author_id=author_id, start=start)
    sayings = None
    if result.get('status') == 'Success':
        sayings = result.get('data')
    return render(request, 'sayings/list.html', {'sayings': sayings})

def get_list_sayings_by_category(request, category_id):
    service = ServiceSayings()
    start = request.query_params.get('start', 0)
    result = service.get_sayings_by_category(category_id=category_id, start=start)
    sayings = None
    if result.get('status') == 'Success':
        sayings = result.get('data')
    return render(request, 'sayings/list.html', {'sayings': sayings})

def get_list_sayings_by_category_author(request, category_id, author_id):
    service = ServiceSayings()
    start = request.query_params.get('start', 0)
    result = service.get_sayings_by_category_author(category_id=category_id, author_id=author_id, start=start)
    sayings = None
    if result.get('status') == 'Success':
        sayings = result.get('data')
    return render(request, 'sayings/list.html', {'sayings': sayings})



