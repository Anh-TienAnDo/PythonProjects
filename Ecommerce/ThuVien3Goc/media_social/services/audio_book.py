import requests
import json
import logging
from .media_social import ServiceMediaSocial
from user.service import JWTUserMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServiceAudioBook():
    def __init__(self, url='http://127.0.0.1:9999/api/audio_books/', request=None):
        self.url = url
        jwt_user_service = JWTUserMiddleware()
        token = jwt_user_service.get_token_in_request(request)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": token,
        }

    def get_all_audiobook(self, start=0, limit=12):
        logger.info("Fetching list of AudioBook starting from %s", start)
        response = requests.get(self.url + f'?_start={start}&_limit={limit}', headers=self.headers, timeout=5)
        media_service = ServiceMediaSocial(response)
        return media_service.check_and_get_data()

    def get_audiobook_by_slug(self, slug):
        logger.info("Fetching details for saying with slug: %s", slug)
        url = self.url + 'detail/' + str(slug) + '/'
        response = requests.get(url, headers=self.headers, timeout=5)
        media_service = ServiceMediaSocial(response)
        return media_service.check_and_get_data()

# start = int(request.GET.get('_start', 0))
# limit = int(request.GET.get('_limit', 12))
# category = request.GET.get('_category', 'all')
# producer = request.GET.get('_producer', 'all')
# author = request.GET.get('_author', 'all')
# time = request.GET.get('_time', 'all')
class AudioBookFilter(ServiceAudioBook):

    def filter(self, author_slug, category_slug, producer_slug, time, start=0, limit=12):
        url = f"{self.url}filter/?_author_slug={author_slug}&_category_slug={category_slug}&_producer_slug={producer_slug}&_time={time}&_start={start}&_limit={limit}"
        response = requests.get(url, headers=self.headers, timeout=5)
        media_service = ServiceMediaSocial(response)
        return media_service.check_and_get_data()

# class AudioBookSearchService(ServiceAudioBook):

#     def search_by_title(self, query, start=0, limit=12):
#         url = self.url + 'search-by-title/'
#         logger.info("Searching AudioBook by title: %s", query)
#         response = requests.get(url + f'?_query={query}&_start={start}&_limit={limit}', headers=self.headers, timeout=5)
#         media_service = ServiceMediaSocial(response)
#         return media_service.check_and_get_data()

#     def search_by_content(self, query, start=0, limit=12):
#         url = self.url + 'search-by-content/'
#         logger.info("Searching AudioBook by content: %s", query)
#         response = requests.get(url + f'?_query={query}&_start={start}&_limit={limit}', headers=self.headers, timeout=5)
#         media_service = ServiceMediaSocial(response)
#         return media_service.check_and_get_data()

#     def search_by_author(self, query, start=0, limit=12):
#         url = self.url + 'search-by-author/'
#         logger.info("Searching AudioBook by author: %s", query)
#         response = requests.get(url + f'?_query={query}&_start={start}&_limit={limit}', headers=self.headers, timeout=5)
#         media_service = ServiceMediaSocial(response)
#         return media_service.check_and_get_data()
