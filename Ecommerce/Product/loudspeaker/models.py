from django.db import models
from django.utils.text import slugify
from producer.models import Producer
from type.models import Type

# Create your models here.
class LoudSpeaker(models.Model):
    name = models.CharField(max_length=255, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    power = models.IntegerField(default=0)
    view = models.IntegerField(default=0)
    producer = models.ForeignKey(Producer, on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    image = models.CharField(max_length=255, null=True)
    price_old = models.IntegerField(default=0)
    price_new = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(LoudSpeaker, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'LoudSpeakers'

