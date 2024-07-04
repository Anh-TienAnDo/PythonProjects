from django.db import models
from author.models import Author
from category.models import Category
from producer.models import Producer

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=255, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    view = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    producer = models.ForeignKey(Producer, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    image = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)
    time_total = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(self.title).lower().replace(' ', '-')
        super(Video, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'videos'

class Episode(models.Model):
    QUALITY = {
        'LD': 'LD-360p',
        'SD': 'SD-480p',
        'HD': 'HD-720p',
        'FHD': 'Full-HD-1080p',
        '2K': '2K',
        '4K': '4K',
    }
    title = models.CharField(max_length=255, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True)
    url = models.TextField()
    quality = models.CharField(max_length=4, choices=QUALITY, default='LD')
    description = models.TextField()
    time = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(self.title).lower().replace(' ', '-')
        super(Episode, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'episodes'
