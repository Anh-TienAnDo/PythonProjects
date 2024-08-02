import requests
import json
from .product import ProductService
from user.service import JWTUserMiddleware

class USBService():
    def __init__(self, request=None):
        self.url = "http://localhost:9998/api/usbs/"
        jwt_user_service = JWTUserMiddleware()
        token = jwt_user_service.get_token_in_request(request)
        self.header = {
            "Content-Type": "application/json",
            "Authorization": token,
        }

    def get_all_usb(self, start=0, limit=12):
        url = f"{self.url}?_start={start}&_limit={limit}"
        response = requests.get(url, headers=self.header, timeout=5)
        return ProductService(response).check_and_get_data()

    def get_usb_by_slug(self, slug):
        url = f"{self.url}detail/{slug}"
        response = requests.get(url, headers=self.header, timeout=5)
        return ProductService(response).check_and_get_data()
    
class USBSearchService(USBService):
    def __init__(self, request):
        super().__init__(request)
        
    def search_usb_by_producer(self, query, start=0, limit=12):
        url = f"{self.url}search-by-producer/?_query={query}&_start={start}&_limit={limit}"
        response = requests.get(url, headers=self.header, timeout=5)
        return ProductService(response).check_and_get_data()
    
    def search_usb_by_name(self, query, start=0, limit=12):
        url = f"{self.url}search-by-name/?_query={query}&_start={start}&_limit={limit}"
        response = requests.get(url, headers=self.header, timeout=5)
        return ProductService(response).check_and_get_data()
    
    
class USBFilterService(USBService):
    def __init__(self, request):
        super().__init__(request)
        
    def filter(self, producer, type_usb, price, start=0, limit=12):
        url = f"{self.url}filter/?_producer={producer}&_type={type_usb}&_price={price}&_start={start}&_limit={limit}"
        response = requests.get(url, headers=self.header, timeout=5)
        product_service = ProductService(response)
        return product_service.check_and_get_data()

    # def create_usb(self, data):
    #     response = requests.post(self.url, json=data)
    #     return response.json()

    # def update_usb(self, id, data):
    #     response = requests.put(f"{self.url}/{id}", json=data)
    #     return response.json()

    # def delete_usb(self, id):
    #     response = requests.delete(f"{self.url}/{id}")
    #     return response.json()
    
