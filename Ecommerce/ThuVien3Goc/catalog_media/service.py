import requests
import json

class ServiceMediaSocial():
    def __init__(self):
        self.url = 'http://127.0.0.1:9999/api/'
        self.headers = {'Content-Type': 'application/json'}
        
    def check_and_get_data(self, response):
        try:
            response = response.json()
            print("-------------------Product----------------------")
            print(str(response))
            if response.get('status') == 'Success':
                return response.get('data')
            else:
                return None
        except json.decoder.JSONDecodeError:
            print('Error: JSONDecodeError. Please check the response. The response is not JSON format.')
            return response.text

    def __str__(self) -> str:
        return self.url
    
class ServiceCategory(ServiceMediaSocial):
    def __init__(self):
        self.url = 'http://127.0.0.1:9999/api/categories/'
        self.headers = {'Content-Type': 'application/json'}

    def get_list_categories(self):
        response = requests.get(self.url, headers=self.headers, timeout=5)
        try:
            response = response.json()
            print(response)
            if response.get('status') == 'Success':
                return response.get('data')
            else:
                return None
        except json.decoder.JSONDecodeError:
            print('Error: JSONDecodeError at get_list_categories. Please check the response. The response is not JSON format.')
            return response.text

    def get_detail_category(self, id):
        response = requests.get(self.url + str(id) + '/', headers=self.headers, timeout=5)
        try:
            response = response.json()
            print(response)
            if response.get('status') == 'Success':
                return response.get('data')
            else:
                return None
        except json.decoder.JSONDecodeError:
            print('Error: JSONDecodeError at get_detail_category. Please check the response. The response is not JSON format.')
            return response.text
    
class ServiceAuthor(ServiceMediaSocial):
    def __init__(self):
        self.url = 'http://127.0.0.1:9999/api/authors/'
        self.headers = {'Content-Type': 'application/json'}

    def get_list_authors(self):
        response = requests.get(self.url, headers=self.headers, timeout=5)
        try:
            response = response.json()
            print(response)
            if response.get('status') == 'Success':
                return response.get('data')
            else:
                return None
        except json.decoder.JSONDecodeError:
            print('Error: JSONDecodeError at get_list_authors. Please check the response. The response is not JSON format.')
            return response.text
    
    def get_detail_author(self, id):
        response = requests.get(self.url + str(id) + '/', headers=self.headers, timeout=5)
        try:
            response = response.json()
            print(response)
            if response.get('status') == 'Success':
                return response.get('data')
            else:
                return None
        except json.decoder.JSONDecodeError:
            print('Error: JSONDecodeError at get_detail_author. Please check the response. The response is not JSON format.')
            return response.text
    
class ServiceProducer(ServiceMediaSocial):
    def __init__(self):
        self.url = 'http://127.0.0.1:9999/api/producers/'
        self.headers = {'Content-Type': 'application/json'}

    def get_list_producers(self):
        response = requests.get(self.url, headers=self.headers, timeout=5)
        try:
            response = response.json()
            print(response)
            if response.get('status') == 'Success':
                return response.get('data')
            else:
                return None
        except json.decoder.JSONDecodeError:
            print('Error: JSONDecodeError at get_list_producers. Please check the response. The response is not JSON format.')
            return response.text
    
    def get_detail_producer(self, id):
        response = requests.get(self.url + str(id) + '/', headers=self.headers, timeout=5)
        try:
            response = response.json()
            print(response)
            if response.get('status') == 'Success':
                return response.get('data')
            else:
                return None
        except json.decoder.JSONDecodeError:
            print('Error: JSONDecodeError at get_detail_producer. Please check the response. The response is not JSON format.')
            return response.text

