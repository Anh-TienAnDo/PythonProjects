import requests
import json
from .service import ServiceMediaSocial
    
class ServiceSayings(ServiceMediaSocial):
    def __init__(self):
        self.url = 'http://127.0.0.1:9999/api/sayings/'
        self.headers = {'Content-Type': 'application/json'}

    def get_list_sayings(self, start):
        response = requests.get(self.url + f'?start={start}', headers=self.headers, timeout=5)
        try:
            response = response.json()
        except json.decoder.JSONDecodeError:
            print('Error: JSONDecodeError at get_list_sayings. Please check the response. The response is not JSON format.')
            return response.text
        return response

    def get_detail_sayings(self, id):
        response = requests.get(self.url + str(id) + '/', headers=self.headers, timeout=5)
        try:
            response = response.json()
        except json.decoder.JSONDecodeError:
            print('Error: JSONDecodeError at get_details_sayings. Please check the response. The response is not JSON format.')
            return response.text
        return response
    
    def get_sayings_by_category(self, category_id, start):
        response = requests.get(self.url + 'category/' + category_id + '/', f'?start={start}', headers=self.headers, timeout=5)
        try:
            response = response.json()
        except json.decoder.JSONDecodeError:
            print('Error: JSONDecodeError at get_sayings_by_category. Please check the response. The response is not JSON format.')
            return response.text
        return response
    
    def get_sayings_by_author(self, author_id, start):
        response = requests.get(self.url + 'author/' + author_id + '/', f'?start={start}', headers=self.headers, timeout=5)
        try:
            response = response.json()
        except json.decoder.JSONDecodeError:
            print('Error: JSONDecodeError at get_sayings_by_author. Please check the response. The response is not JSON format.')
            return response.text
        return response
    
    def get_sayings_by_category_author(self, category_id, author_id, start):
        response = requests.get(self.url + 'category/' + category_id + '/author/' + author_id + '/', f'?start={start}', headers=self.headers, timeout=5)
        try:
            response = response.json()
        except json.decoder.JSONDecodeError:
            print('Error: JSONDecodeError at get_sayings_by_category_author. Please check the response. The response is not JSON format.')
            return response.text
        return response
    
