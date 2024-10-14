import requests
import json
import logging
from user.service import JWTUserMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
    
class CategoryService():
    def __init__(self, url='http://127.0.0.1:9999/api/categories', request=None):
        self.url = url
        jwt_user_service = JWTUserMiddleware()
        token = jwt_user_service.get_token_in_request(request)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": token,
        }

    def get_list_category(self):
        response = requests.get(self.url, headers=self.headers, timeout=5)
        try:
            response = response.json()
            if response.get('status') == 'Success' and len(response.get('data')) > 0:
                return response.get('data')
            else:
                return None
        except json.decoder.JSONDecodeError:
            print('Error: JSONDecodeError at get_list_categorie. Please check the response. The response is not JSON format.')
            return response.text

    
class AuthorService():
    def __init__(self, url='http://127.0.0.1:9999/api/authors', request=None):
        self.url = url
        jwt_user_service = JWTUserMiddleware()
        token = jwt_user_service.get_token_in_request(request)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": token,
        }

    def get_list_author(self):
        response = requests.get(self.url, headers=self.headers, timeout=5)
        try:
            response = response.json()
            print("--------------")
            print(response)
            if response.get('status') == 'Success' and len(response.get('data')) > 0:
                return response.get('data')
            else:
                return None
        except json.decoder.JSONDecodeError:
            print('Error: JSONDecodeError at get_list_author. Please check the response. The response is not JSON format.')
            return response.text

    
class ProducerService():
    def __init__(self, url='http://127.0.0.1:9999/api/producers', request=None):
        self.url = url
        jwt_user_service = JWTUserMiddleware()
        token = jwt_user_service.get_token_in_request(request)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": token,
        }

    def get_list_producer(self):
        response = requests.get(self.url, headers=self.headers, timeout=5)
        try:
            response = response.json()
            if response.get('status') == 'Success' and len(response.get('data')) > 0:
                return response.get('data')
            else:
                return None
        except json.decoder.JSONDecodeError:
            print('Error: JSONDecodeError at get_list_producers. Please check the response. The response is not JSON format.')
            return response.text
    
    # def get_detail_producer(self, id):
    #     response = requests.get(self.url + str(id) + '/', headers=self.headers, timeout=5)
    #     try:
    #         response = response.json()
    #         print(response)
    #         if response.get('status') == 'Success':
    #             return response.get('data')
    #         else:
    #             return None
    #     except json.decoder.JSONDecodeError:
    #         print('Error: JSONDecodeError at get_detail_producer. Please check the response. The response is not JSON format.')
    #         return response.text

