import requests
import json

class LoudspeakerService():
    def __init__(self):
        self.url = "http://127.0.0.1:9998/api/loudspeakers/"
        self.header = {
            # "Content-Type": "application/json"
        }

    def get_all_loudspeaker(self, start=0, limit=12):
        url = f"{self.url}?_start={start}&_limit={limit}"
        response = requests.get(url, headers=self.header, timeout=5)
        return response.json()

    def get_loudspeaker_by_slug(self, slug):
        url = f"{self.url}detail/{slug}"
        response = requests.get(url, headers=self.header, timeout=5)
        return response.json()

class LoudspeakerSearchService(LoudspeakerService):
    def __init__(self):
        super().__init__()

    def search_loudspeaker_by_producer(self, query, start=0, limit=12):
        url = f"{self.url}search-by-producer/" + f"?_query={query}&_start={start}&_limit={limit}"
        response = requests.get(url=url, headers=self.header, timeout=5)
        return response.json()

    def search_loudspeaker_by_name(self, query, start=0, limit=12):
        url = f"{self.url}search-by-name/" + f"?_query={query}&_start={start}&_limit={limit}"
        response = requests.get(url=url, headers=self.header)
        return response.json()

class LoudspeakerFilterService(LoudspeakerService):
    def __init__(self):
        super().__init__()

    def filter(self, producer, type, price, start=0, limit=12):
        url = f"{self.url}filter/?_producer={producer}&_type={type}&_price={price}&_start={start}&_limit={limit}"
        response = requests.get(url, headers=self.header, timeout=5)
        return response.json()

loudspeaker_service = LoudspeakerService()
print(loudspeaker_service.get_all_loudspeaker().get('data'))
print("-----------------------------------------------------")
loudspeaker_search_service = LoudspeakerSearchService()
print(loudspeaker_search_service.search_loudspeaker_by_name(query='Loa'))