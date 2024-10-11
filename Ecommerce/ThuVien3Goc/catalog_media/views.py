import logging
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .services import *
from ThuVien3Goc.settings import MEDIASOCIAL_TYPE

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create your views here.
def get_list_author(request):
    logger.info("Fetching list of authors")
    service = AuthorService(request=request)
    authors = service.get_list_author()
    logger.info("Fetched authors: %s", authors)
    content = {
        'authors': authors
    }
    return JsonResponse(data=content)
    # return render(request, 'author/list.html', {'authors': authors})


def get_list_category(request):
    logger.info("Fetching list of categories")
    service = CategoryService(request=request)
    categories = service.get_list_category()
    logger.info("Fetched categories: %s", categories)
    return render(request, 'category/list.html', {'categories': categories})

# def get_detail_category(request, id):
#     logger.info("Fetching details for category with id: %s", id)
#     service = ServiceCategory()
#     category = service.get_detail_category(id)
#     logger.info("Fetched category details: %s", category)
#     return render(request, 'category/detail.html', {'category': category})


def get_list_producer(request):
    logger.info("Fetching list of producers")
    service = ProducerService(request=request)
    producers = service.get_list_producer()
    logger.info("Fetched producer: %s", producers)
    return render(request, 'producer/list.html', {'producers': producers})

def get_list_type(request):
    logger.info("Fetching list of types")
    types = MEDIASOCIAL_TYPE
    logger.info("Fetched types: %s", types)
    return render(request, 'type/list.html', {'types': types})
