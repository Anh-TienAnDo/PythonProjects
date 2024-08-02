import requests
import json
from .product import ProductService
from user.service import JWTUserMiddleware

class MemoryStickService():
    def __init__(self, request=None):
        self.url = "http://localhost:9998/api/memory_sticks/"
        jwt_user_service = JWTUserMiddleware()
        token = jwt_user_service.get_token_in_request(request)
        self.header = {
            "Content-Type": "application/json",
            "Authorization": token,
        }

    def get_all_memory_stick(self, start=0, limit=12):
        url = f"{self.url}?_start={start}&_limit={limit}"
        response = requests.get(url, headers=self.header, timeout=5)
        product_service = ProductService(response)
        return product_service.check_and_get_data()

    def get_memory_stick_by_slug(self, slug):
        url = f"{self.url}detail/{slug}"
        response = requests.get(url, headers=self.header, timeout=5)
        product_service = ProductService(response)
        return product_service.check_and_get_data()

class MemoryStickSearchService(MemoryStickService):
    def __init__(self, request):
        super().__init__(request)
        
    def search_memory_stick_by_producer(self, query, start=0, limit=12):
        url = f"{self.url}search-by-producer/?_query={query}&_start={start}&_limit={limit}"
        response = requests.get(url, headers=self.header, timeout=5)
        product_service = ProductService(response)
        return product_service.check_and_get_data()
    
    def search_memory_stick_by_name(self, query, start=0, limit=12):
        url = f"{self.url}search-by-name/?_query={query}&_start={start}&_limit={limit}"
        response = requests.get(url, headers=self.header, timeout=5)
        product_service = ProductService(response)
        return product_service.check_and_get_data()
    
class MemoryStickFilterService(MemoryStickService):
    def __init__(self, request):
        super().__init__(request)
        
    def filter(self, producer, type_memorystick, price, start=0, limit=12):
        url = f"{self.url}filter/?_producer={producer}&_type={type_memorystick}&_price={price}&_start={start}&_limit={limit}"
        response = requests.get(url, headers=self.header, timeout=5)
        product_service = ProductService(response)
        return product_service.check_and_get_data()

    # def create_memory_stick(self, data):
    #     response = requests.post(self.url, json=data)
    #     return response.json()

    # def update_memory_stick(self, id, data):
    #     response = requests.put(f"{self.url}/{id}", json=data)
    #     return response.json()

    # def delete_memory_stick(self, id):
    #     response = requests.delete(f"{self.url}/{id}")
    #     return response.json()
    
