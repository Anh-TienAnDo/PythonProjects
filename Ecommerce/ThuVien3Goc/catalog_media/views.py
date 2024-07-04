from django.shortcuts import render
from django.http import HttpResponse
from .service import ServiceAuthor, ServiceCategory
# Create your views here.
def get_list_author(request):
    service = ServiceAuthor()
    authors = service.get_list_authors()
    return render(request, 'author/list.html', {'authors': authors})

def get_detail_author(request, id):
    service = ServiceAuthor()
    author = service.get_detail_author(id)
    return render(request, 'author/detail.html', {'author': author})

def get_list_category(request):
    service = ServiceCategory()
    categories = service.get_list_categories()
    return render(request, 'category/list.html', {'categories': categories})

def get_detail_category(request, id):
    service = ServiceCategory()
    category = service.get_detail_category(id)
    return render(request, 'category/detail.html', {'category': category})
