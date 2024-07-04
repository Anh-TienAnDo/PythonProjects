from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255, null=True)
    slug = models.SlugField(null=True, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(self.name).replace(' ', '-').lower()
        super(Author, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = 'Authors'

