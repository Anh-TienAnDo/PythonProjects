import requests
import json
from .product import ProductService
from user.service import JWTUserMiddleware

# b1 làm template tags -> gắn vào html -> tạo view trong product type và producer -> call api từ sẻvice product
# b2: taọ các filter trong product sẻvice -> call api từ product service trong service product
class LoudspeakerService():
    def __init__(self, request=None):
        self.url = "http://127.0.0.1:9998/api/loudspeakers/"
        jwt_user_service = JWTUserMiddleware()
        token = jwt_user_service.get_token_in_request(request)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": token,
        }
        
    def get_all_loudspeaker(self, start=0, limit=12):
        url = f"{self.url}?_start={start}&_limit={limit}"
        response = requests.get(url, headers=self.headers, timeout=5)
        product_service = ProductService(response)
        return product_service.check_and_get_data()

    def get_loudspeaker_by_slug(self, slug):
        url = f"{self.url}detail/{slug}"
        response = requests.get(url, headers=self.headers, timeout=5)
        product_service = ProductService(response)
        return product_service.check_and_get_data()
    
class LoudspeakerSearchService(LoudspeakerService):
    def __init__(self, request):
        super().__init__(request)
    
    def search_loudspeaker_by_producer(self, query, start=0, limit=12):
        url = f"{self.url}search-by-producer/?_query={query}&_start={start}&_limit={limit}"
        response = requests.get(url, headers=self.headers, timeout=5)
        product_service = ProductService(response)
        return product_service.check_and_get_data()
    
    def search_loudspeaker_by_name(self, query, start=0, limit=12):
        url = f"{self.url}search-by-name/?_query={query}&_start={start}&_limit={limit}"
        response = requests.get(url, headers=self.headers, timeout=5)
        product_service = ProductService(response)
        return product_service.check_and_get_data()
    
class LoudspeakerFilterService(LoudspeakerService):
    def __init__(self, request):
        super().__init__(request)
        
    def filter(self, producer, type_loudspeaker, price, start=0, limit=12):
        url = f"{self.url}filter/?_producer={producer}&_type={type_loudspeaker}&_price={price}&_start={start}&_limit={limit}"
        response = requests.get(url, headers=self.headers, timeout=5)
        product_service = ProductService(response)
        return product_service.check_and_get_data()


    # def create_loudspeaker(self, data):
    #     response = requests.post(self.url, json=data)
    #     return response.json()

    # def update_loudspeaker(self, id, data):
    #     response = requests.put(f"{self.url}/{id}", json=data)
    #     return response.json()

    # def delete_loudspeaker(self, id):
    #     response = requests.delete(f"{self.url}/{id}")
    #     return response.json()
    
