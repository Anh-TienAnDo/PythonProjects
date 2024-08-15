import requests
import json

class ProductService():
    def __init__(self, response):
        self.response = response

    def check_and_get_data(self):
        try:
            response = self.response.json()
            # print("-------------------Product----------------------")
            # print(str(response))
            if response.get('status') == 'Success':
                return response.get('data')
            else:
                return None
        except json.decoder.JSONDecodeError:
            print('Error: JSONDecodeError. Please check the response. The response is not JSON format.')
            return response.text

class ProductTypeService():
    def __init__(self):
        self.url = "http://127.0.0.1:9998/api/types/"
        self.header = {
            "Content-Type": "application/json"
        }
    
    def get_all_product_type(self):
        response = requests.get(self.url, headers=self.header, timeout=5)
        product_service = ProductService(response)
        return product_service.check_and_get_data()

class ProductProducerService():
    def __init__(self):
        self.url = "http://127.0.0.1:9998/api/producers/"
        self.header = {
            "Content-Type": "application/json"
        }
    
    def get_all_product_producer(self):
        response = requests.get(self.url, headers=self.header, timeout=5)
        product_service = ProductService(response)
        return product_service.check_and_get_data()