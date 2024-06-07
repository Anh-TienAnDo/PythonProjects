from djongo import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True,
                            help_text='Unique value for product page URL, created from name.', null=True)
    description = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    # meta_keywords = models.CharField("Meta Keywords", max_length=255,
    #                                  help_text='Comma-delimited set of SEO keywords for meta tag')
    # meta_description = models.CharField("Meta Description", max_length=255,
    #                                     help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'catalog'

    def __str__(self):
        return self.name


