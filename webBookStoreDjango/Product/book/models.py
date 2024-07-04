from djongo import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True,
        help_text='Unique value for product page URL, created from name.', null=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True)
    price = models.IntegerField(default=0)
    old_price = models.IntegerField(default=0)
    image = models.TextField()
    # thumbnail = models.ImageField(upload_to='images/products/thumbnails')
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # categories = models.ArrayReferenceField(to=Category, on_delete=models.CASCADE, null=True)
    categories = models.ManyToManyField(to=Category)


    def __str__(self):
        return self.name

    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None

