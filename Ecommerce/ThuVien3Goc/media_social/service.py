import requests
import json
import logging
from user.service import JWTUserMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MediaSocialService:
    def __init__(self, url='http://127.0.0.1:9999/api/media-socials', request=None):
        self.url = url
        jwt_user_service = JWTUserMiddleware()
        token = jwt_user_service.get_token_in_request(request)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": token,
        }

    def check_and_get_data(self, response):
        try:
            response = response.json()
            logger.info("Media response: %s", str(response))
            # print(response)
            if response.get('status') == 'Success' and len(response.get('data')) > 0:
                return response
            else:
                return response
        except json.decoder.JSONDecodeError:
            logger.error('JSONDecodeError. Please check the response. The response is not JSON format.')
            return response.text
        
    def get_all(self, start=0, limit=12):
        logger.info("Fetching list of media social starting from %s", start)
        response = requests.get(self.url + f'?_start={start}&_limit={limit}', headers=self.headers, timeout=5)
        return self.check_and_get_data(response=response)
        
    def get_detail(self, type_media, slug):
        logger.info("Fetching details for media social with slug: %s", slug)
        url = self.url + 'details/' + str(type_media) + '/' + str(slug)
        response = requests.get(url, headers=self.headers, timeout=5)
        return self.check_and_get_data(response=response)

    # def get_all_sayings(self, start=0, limit=12):
    #     logger.info("Fetching list of sayings starting from %s", start)
    #     response = requests.get(self.url + f'?_start={start}&_limit={limit}', headers=self.headers, timeout=5)
    #     media_service = ServiceMediaSocial(response)
    #     return media_service.check_and_get_data()

    # def get_sayings_by_slug(self, slug):
    #     logger.info("Fetching details for saying with slug: %s", slug)
    #     url = self.url + 'detail/' + str(slug) + '/'
    #     response = requests.get(url, headers=self.headers, timeout=5)
    #     media_service = ServiceMediaSocial(response)
    #     return media_service.check_and_get_data()


class MediaSocialFilterService(MediaSocialService):
    def __init__(self, url='http://127.0.0.1:9999/api/media-socials/filter', request=None):
        super().__init__(url, request)
        self.author_name = str(request.GET.get('author_name', ''))
        self.category_name = str(request.GET.get('category_name', ''))
        self.producer_name = str(request.GET.get('producer_name', ''))
        self.time_total = str(request.GET.get('time_total', 0))
    
    def filter(self, type_media, start=0, limit=12):
        url = f"{self.url}?_type={type_media}&_author_name={self.author_name}&_category_name={self.category_name}&_producer_name={self.producer_name}&_time_total={self.time_total}&_start={start}&_limit={limit}"
        response = requests.get(url, headers=self.headers, timeout=5)
        return self.check_and_get_data(response=response)

class MediaSocialSearchAndFilterService(MediaSocialService):
    def __init__(self, url='http://127.0.0.1:9999/api/media-socials/search-filter', request=None):
        super().__init__(url, request)
        self.query = str(request.GET.get('query', ''))
        self.author_name = str(request.GET.get('author_name', ''))
        self.category_name = str(request.GET.get('category_name', ''))
        self.producer_name = str(request.GET.get('producer_name', ''))
        self.type_media = str(request.GET.get('type_media', ''))
        self.time_total = str(request.GET.get('time_total', 0))
        
    def search_and_filter(self, start=0, limit=12):
        url = f"{self.url}?_query={self.query}&_author_name={self.author_name}&_category_name={self.category_name}&_producer_name={self.producer_name}&_type={self.type_media}&_time_total={self.time_total}&_start={start}&_limit={limit}"
        response = requests.get(url, headers=self.headers, timeout=5)
        return self.check_and_get_data(response=response)


    

        
        
        
