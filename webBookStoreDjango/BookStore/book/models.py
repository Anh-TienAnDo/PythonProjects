

class Category():
    def __init__(self, data):
        self.id = data['id']
        self.name = data.get('name')
        self.slug = data.get('slug')
        self.is_active = data.get('is_active')
        self.description = data.get('description')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')

    # class Meta:
    #     abstract = True

    def __str__(self):
        return self.name

class Book():
    def __init__(self, data):
        self.id = data['id']
        self.name = data.get('name')
        self.slug = data.get('slug')
        self.categories = data.get('categories')
        self.author = data.get('author')
        self.publisher = data.get('publisher')
        self.price = data.get('price')
        self.image = data.get('image')
        self.is_active = data.get('is_active')
        self.description = data.get('description')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')


    def __str__(self):
        return self.name

