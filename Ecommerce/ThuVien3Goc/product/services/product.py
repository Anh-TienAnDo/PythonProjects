import requests
import json

class ProductService():
    def __init__(self, response):
        self.response = response

    def check_and_get_data(self):
        try:
            response = self.response.json()
            print(response)
            if response.get('status') == 'Success':
                return response.get('data')
            else:
                return None
        except json.decoder.JSONDecodeError:
            print('Error: JSONDecodeError. Please check the response. The response is not JSON format.')
            return response.text