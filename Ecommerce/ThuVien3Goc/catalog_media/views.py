import logging
from django.shortcuts import render
from django.http import HttpResponse
from .services import ServiceAuthor, ServiceCategory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create your views here.
def get_list_author(request):
    logger.info("Fetching list of authors")
    service = ServiceAuthor(request=request)
    authors = service.get_list_authors()
    logger.info("Fetched authors: %s", authors)
    return render(request, 'author/list.html', {'authors': authors})

# def get_detail_author(request, id):
#     logger.info("Fetching details for author with id: %s", id)
#     service = ServiceAuthor()
#     author = service.get_detail_author(id)
#     logger.info("Fetched author details: %s", author)
#     return render(request, 'author/detail.html', {'author': author})

def get_list_category(request):
    logger.info("Fetching list of categories")
    service = ServiceCategory(request=request)
    categories = service.get_list_categories()
    logger.info("Fetched categories: %s", categories)
    return render(request, 'category/list.html', {'categories': categories})

# def get_detail_category(request, id):
#     logger.info("Fetching details for category with id: %s", id)
#     service = ServiceCategory()
#     category = service.get_detail_category(id)
#     logger.info("Fetched category details: %s", category)
#     return render(request, 'category/detail.html', {'category': category})


# from django.shortcuts import render
# from django.http import HttpResponse
# from .service import ServiceAuthor, ServiceCategory
# # Create your views here.
# def get_list_author(request):
#     service = ServiceAuthor()
#     authors = service.get_list_authors()
#     return render(request, 'author/list.html', {'authors': authors})

# def get_detail_author(request, id):
#     service = ServiceAuthor()
#     author = service.get_detail_author(id)
#     return render(request, 'author/detail.html', {'author': author})

# def get_list_category(request):
#     service = ServiceCategory()
#     categories = service.get_list_categories()
#     return render(request, 'category/list.html', {'categories': categories})

# def get_detail_category(request, id):
#     service = ServiceCategory()
#     category = service.get_detail_category(id)
#     return render(request, 'category/detail.html', {'category': category})
