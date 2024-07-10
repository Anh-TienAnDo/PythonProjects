import requests
import json
from .product import ProductService


class LoudspeakerService():
    def __init__(self):
        self.url = "http://localhost:9998/api/loudspeakers/"
        self.header = {
            "Content-Type": "application/json"
        }

    def get_all_loudspeaker(self, start=0, limit=12):
        url = f"{self.url}?_start={start}&_limit={limit}"
        response = requests.get(url, headers=self.header, timeout=5)
        return ProductService(response).check_and_get_data()

    def get_loudspeaker_by_slug(self, slug):
        url = f"{self.url}{slug}"
        response = requests.get(url, headers=self.header, timeout=5)
        return ProductService(response).check_and_get_data()

    # def create_loudspeaker(self, data):
    #     response = requests.post(self.url, json=data)
    #     return response.json()

    # def update_loudspeaker(self, id, data):
    #     response = requests.put(f"{self.url}/{id}", json=data)
    #     return response.json()

    # def delete_loudspeaker(self, id):
    #     response = requests.delete(f"{self.url}/{id}")
    #     return response.json()
    
