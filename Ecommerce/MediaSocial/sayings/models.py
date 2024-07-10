from django.db import models
from author.models import Author
from category.models import Category
from django.utils.text import slugify

# Create your models here.
class Saying(models.Model):
    title = models.CharField(max_length=255, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    text = models.TextField()
    view = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    categories = models.ManyToManyField(Category)
    image = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.text)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Saying, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Sayings'
