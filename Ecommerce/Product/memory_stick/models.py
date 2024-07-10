from django.db import models
from django.utils.text import slugify
from producer.models import Producer
from type.models import Type

# Create your models here.
class MemoryStick(models.Model):
    MEMORY = {
        "1": "1GB",
        "2": "2GB",
        "4": "4GB",
        "8": "8GB",
        "16": "16GB",
        "32": "32GB",
        "64": "64GB",
        "128": "128GB",
        "256": "256GB",
        "512": "512GB",
        "1024": "1024GB",
    }
    name = models.CharField(max_length=255, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    view = models.IntegerField(default=0)
    producer = models.ForeignKey(Producer, on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    image = models.CharField(max_length=255, null=True)
    price_old = models.IntegerField(default=0)
    price_new = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    memory = models.CharField(max_length=10, choices=MEMORY, default="16")
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(MemoryStick, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'MemorySticks'


