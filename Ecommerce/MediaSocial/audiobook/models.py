from django.db import models
from author.models import Author
from category.models import Category
from producer.models import Producer

# Create your models here.
class AudioBook(models.Model):
    title = models.CharField(max_length=255, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    view = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    categories = models.ManyToManyField(Category)
    producer = models.ForeignKey(Producer, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    image = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)
    time_total = models.IntegerField(default=0)
    # voice = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(self.title).lower().replace(' ', '-')
        super(AudioBook, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'audio_books'

class BookSection(models.Model):
    TYPEFILE = {
        'mp3': 'mp3',
        'wav': 'wav',
        'ogg': 'ogg',
    }
    title = models.CharField(max_length=255, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    audio_book = models.ForeignKey(AudioBook, on_delete=models.SET_NULL, null=True)
    # url = models.TextField()
    # url = models.FileField(upload_to='audio_books/')
    url = models.CharField(max_length=255)
    file_type = models.CharField(max_length=4, choices=TYPEFILE, default='mp3')
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
        super(BookSection, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'book_sections'

