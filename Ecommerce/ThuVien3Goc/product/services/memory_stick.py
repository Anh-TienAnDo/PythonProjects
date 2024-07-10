import requests
import json
from .product import ProductService

class MemoryStickService():
    def __init__(self):
        self.url = "http://localhost:9998/api/memory_sticks/"
        self.header = {
            "Content-Type": "application/json"
        }

    def get_all_memory_stick(self, start=0, limit=12):
        url = f"{self.url}?_start={start}&_limit={limit}"
        response = requests.get(url, headers=self.header, timeout=5)
        return ProductService(response).check_and_get_data()

    def get_memory_stick_by_slug(self, slug):
        url = f"{self.url}{slug}"
        response = requests.get(url, headers=self.header, timeout=5)
        return ProductService(response).check_and_get_data()


    # def create_memory_stick(self, data):
    #     response = requests.post(self.url, json=data)
    #     return response.json()

    # def update_memory_stick(self, id, data):
    #     response = requests.put(f"{self.url}/{id}", json=data)
    #     return response.json()

    # def delete_memory_stick(self, id):
    #     response = requests.delete(f"{self.url}/{id}")
    #     return response.json()
    
