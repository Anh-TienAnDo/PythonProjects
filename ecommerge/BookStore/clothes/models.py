from djongo import models

# Create your models here.

class Clothes():
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.slug = data['slug']
        self.producer_id = data['producer_id']
        self.type_id = data['type_id']
        self.price = data['price']
        self.image = data['image']
        self.is_active = data['is_active']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    def __str__(self):
        return self.name
