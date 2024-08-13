import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServiceMediaSocial():
    def __init__(self, response):
        self.response = response
        
    def check_and_get_data(self):
        try:
            response = self.response.json()
            logger.info("Media response: %s", str(response))
            print(response)
            if response.get('status') == 'Success':
                return response.get('data')
            else:
                return None
        except json.decoder.JSONDecodeError:
            logger.error('JSONDecodeError. Please check the response. The response is not JSON format.')
            return response.text
