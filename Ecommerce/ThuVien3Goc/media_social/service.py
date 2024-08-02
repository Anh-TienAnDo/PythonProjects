import requests
import json
import logging
from catalog_media.service import ServiceMediaSocial

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServiceSayings(ServiceMediaSocial):
    def __init__(self, url='http://127.0.0.1:9999/api/sayings/'):
        self.url = url
        self.headers = {'Content-Type': 'application/json'}

    def get_list_sayings(self, start):
        logger.info("Fetching list of sayings starting from %s", start)
        response = requests.get(self.url + f'?start={start}', headers=self.headers, timeout=5)
        try:
            response = response.json()
            logger.info("Response: %s", str(response)[0:200])
            if response.get('status') == 'Success':
                return response.get('data')
            else:
                return None
        except json.decoder.JSONDecodeError:
            logger.error('JSONDecodeError at get_list_sayings. Response is not JSON format.')
            return response.text

    def get_detail_sayings(self, slug):
        logger.info("Fetching details for saying with slug: %s", slug)
        response = requests.get(self.url + str(slug) + '/', headers=self.headers, timeout=5)
        try:
            response = response.json()
            logger.info("Response: %s", str(response)[0:200])
            if response.get('status') == 'Success':
                return response.get('data')
            else:
                return None
        except json.decoder.JSONDecodeError:
            logger.error('JSONDecodeError at get_detail_sayings. Response is not JSON format.')
            return response.text

    def get_sayings_by_category(self, category_slug, start):
        logger.info("Fetching sayings for category: %s starting from %s", category_slug, start)
        response = requests.get(self.url + 'category/' + category_slug + '/', f'?start={start}', headers=self.headers, timeout=5)
        try:
            response = response.json()
            logger.info("Response: %s", str(response)[0:200])
            if response.get('status') == 'Success':
                return response.get('data')
            else:
                return None
        except json.decoder.JSONDecodeError:
            logger.error('JSONDecodeError at get_sayings_by_category. Response is not JSON format.')
            return response.text

    def get_sayings_by_author(self, author_slug, start):
        logger.info("Fetching sayings for author: %s starting from %s", author_slug, start)
        response = requests.get(self.url + 'author/' + author_slug + '/', f'?start={start}', headers=self.headers, timeout=5)
        try:
            response = response.json()
            logger.info("Response: %s", str(response)[0:200])
            if response.get('status') == 'Success':
                return response.get('data')
            else:
                return None
        except json.decoder.JSONDecodeError:
            logger.error('JSONDecodeError at get_sayings_by_author. Response is not JSON format.')
            return response.text

    def get_sayings_by_category_author(self, category_slug, author_slug, start):
        logger.info("Fetching sayings for category: %s and author: %s starting from %s", category_slug, author_slug, start)
        response = requests.get(self.url + 'category/' + category_slug + '/author/' + author_slug + '/', f'?start={start}', headers=self.headers, timeout=5)
        try:
            response = response.json()
            logger.info("Response: %s", str(response)[0:200])
            if response.get('status') == 'Success':
                return response.get('data')
            else:
                return None
        except json.decoder.JSONDecodeError:
            logger.error('JSONDecodeError at get_sayings_by_category_author. Response is not JSON format.')
            return response.text

class SayingsFilter:
    def __init__(self, request):
        self.request = request

    def filter_sayings(self):
        start = int(self.request.GET.get('start', 0))
        author_slug = str(self.request.GET.get('author_slug', 'all'))
        category_slug = str(self.request.GET.get('category_slug', 'all'))
        service = ServiceSayings()
        sayings = []
        if author_slug != 'all' and category_slug != 'all':
            sayings = service.get_sayings_by_category_author(category_slug=category_slug, author_slug=author_slug, start=start)
        elif author_slug != 'all':
            sayings = service.get_sayings_by_author(author_slug=author_slug, start=start)
        elif category_slug != 'all':
            sayings = service.get_sayings_by_category(category_slug=category_slug, start=start)
        else:
            sayings = service.get_list_sayings(start=start)
        return sayings

class SayingsSearchService(ServiceSayings):
    def __init__(self):
        super().__init__()

    def search_by_title(self, query, start=0, limit=12):
        url = self.url + 'search-by-title/'
        logger.info("Searching sayings by title: %s", query)
        response = requests.get(url + f'?_query={query}&_start={start}&_limit={limit}', headers=self.headers, timeout=5)
        return self.check_and_get_data(response)

    def search_by_content(self, query, start=0, limit=12):
        url = self.url + 'search-by-content/'
        logger.info("Searching sayings by content: %s", query)
        response = requests.get(url + f'?_query={query}&_start={start}&_limit={limit}', headers=self.headers, timeout=5)
        return self.check_and_get_data(response)

    def search_by_author(self, query, start=0, limit=12):
        url = self.url + 'search-by-author/'
        logger.info("Searching sayings by author: %s", query)
        response = requests.get(url + f'?_query={query}&_start={start}&_limit={limit}', headers=self.headers, timeout=5)
        return self.check_and_get_data(response)



# import requests
# import json
# from catalog_media.service import ServiceMediaSocial
    
# class ServiceSayings(ServiceMediaSocial):
#     def __init__(self, url='http://127.0.0.1:9999/api/sayings/'):
#         self.url = url
#         self.headers = {'Content-Type': 'application/json'}

#     def get_list_sayings(self, start):
#         response = requests.get(self.url + f'?start={start}', headers=self.headers, timeout=5)
#         try:
#             response = response.json()
#             print("-------------------Media----------------------")
#             print(str(response)[0:200])
#             if response.get('status') == 'Success':
#                 return response.get('data')
#             else:
#                 return None
#         except json.decoder.JSONDecodeError:
#             print('Error: JSONDecodeError at get_list_sayings. Please check the response. The response is not JSON format.')
#             return response.text

#     def get_detail_sayings(self, slug):
#         response = requests.get(self.url + str(slug) + '/', headers=self.headers, timeout=5)
#         try:
#             response = response.json()
#             print("-------------------Media----------------------")
#             print(str(response)[0:200])
#             if response.get('status') == 'Success':
#                 return response.get('data')
#             else:
#                 return None
#         except json.decoder.JSONDecodeError:
#             print('Error: JSONDecodeError at get_details_sayings. Please check the response. The response is not JSON format.')
#             return response.text
    
#     def get_sayings_by_category(self, category_slug, start):
#         response = requests.get(self.url + 'category/' + category_slug + '/', f'?start={start}', headers=self.headers, timeout=5)
#         try:
#             response = response.json()
#             print("-------------------Media----------------------")
#             print(str(response)[0:200])
#             if response.get('status') == 'Success':
#                 return response.get('data')
#             else:
#                 return None
#         except json.decoder.JSONDecodeError:
#             print('Error: JSONDecodeError at get_sayings_by_category. Please check the response. The response is not JSON format.')
#             return response.text
    
#     def get_sayings_by_author(self, author_slug, start):
#         response = requests.get(self.url + 'author/' + author_slug + '/', f'?start={start}', headers=self.headers, timeout=5)
#         try:
#             response = response.json()
#             print("-------------------Media----------------------")
#             print(str(response)[0:200])
#             if response.get('status') == 'Success':
#                 return response.get('data')
#             else:
#                 return None
#         except json.decoder.JSONDecodeError:
#             print('Error: JSONDecodeError at get_sayings_by_author. Please check the response. The response is not JSON format.')
#             return response.text
    
#     def get_sayings_by_category_author(self, category_slug, author_slug, start):
#         response = requests.get(self.url + 'category/' + category_slug + '/author/' + author_slug + '/', f'?start={start}', headers=self.headers, timeout=5)
#         try:
#             response = response.json()
#             print("-------------------Media----------------------")
#             print(str(response)[0:200])
#             if response.get('status') == 'Success':
#                 return response.get('data')
#             else:
#                 return None
#         except json.decoder.JSONDecodeError:
#             print('Error: JSONDecodeError at get_sayings_by_category_author. Please check the response. The response is not JSON format.')
#             return response.text
    
# class SayingsFilter:
#     def __init__(self, request):
#         self.request = request
    
#     def filter_sayings(self):
#         start = int(self.request.GET.get('start', 0))
#         author_slug = str(self.request.GET.get('author_slug', 'all'))
#         category_slug = str(self.request.GET.get('category_slug', 'all'))
#         service = ServiceSayings()
#         sayings = []
#         if author_slug != 'all' and category_slug != 'all':
#             sayings = service.get_sayings_by_category_author(category_slug=category_slug, author_slug=author_slug, start=start)
#         elif author_slug != 'all':
#             sayings = service.get_sayings_by_author(author_slug=author_slug, start=start)
#         elif category_slug != 'all':
#             sayings = service.get_sayings_by_category(category_slug=category_slug, start=start)
#         else:
#             sayings = service.get_list_sayings(start=start)
#         return sayings
    
# class SayingsSearchService(ServiceSayings):
#     def __init__(self):
#         super().__init__()
        
#     def search_by_title(self, query, start=0, limit=12):
#         url = self.url + 'search-by-title/'
#         response = requests.get(url + f'?_query={query}&_start={start}&_limit={limit}', headers=self.headers, timeout=5)
#         return self.check_and_get_data(response)
    
#     def search_by_content(self, query, start=0, limit=12):
#         url = self.url + 'search-by-content/'
#         response = requests.get(url + f'?_query={query}&_start={start}&_limit={limit}', headers=self.headers, timeout=5)
#         return self.check_and_get_data(response)
    
#     def search_by_author(self, query, start=0, limit=12):
#         url = self.url + 'search-by-author/'
#         response = requests.get(url + f'?_query={query}&_start={start}&_limit={limit}', headers=self.headers, timeout=5)
#         return self.check_and_get_data(response)
        
        
        
