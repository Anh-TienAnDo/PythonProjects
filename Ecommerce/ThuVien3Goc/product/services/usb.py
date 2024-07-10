import requests
import json
from .product import ProductService

class USBService():
    def __init__(self):
        self.url = "http://localhost:9998/api/usbs/"
        self.header = {
            "Content-Type": "application/json"
        }

    def get_all_usb(self, start=0, limit=12):
        url = f"{self.url}?_start={start}&_limit={limit}"
        response = requests.get(url, headers=self.header, timeout=5)
        return ProductService(response).check_and_get_data()

    def get_usb_by_slug(self, slug):
        url = f"{self.url}{slug}"
        response = requests.get(url, headers=self.header, timeout=5)
        return ProductService(response).check_and_get_data()

    # def create_usb(self, data):
    #     response = requests.post(self.url, json=data)
    #     return response.json()

    # def update_usb(self, id, data):
    #     response = requests.put(f"{self.url}/{id}", json=data)
    #     return response.json()

    # def delete_usb(self, id):
    #     response = requests.delete(f"{self.url}/{id}")
    #     return response.json()
    
