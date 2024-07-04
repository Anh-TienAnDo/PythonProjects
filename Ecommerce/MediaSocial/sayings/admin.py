from django.contrib import admin
from .models import Saying
from django.utils.text import slugify
db_name = "default"

# Register your models here.
class SayingAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'view', 'author', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('title',)
    list_filter = ('author', 'is_active')
    search_fields = ('title', 'author')
    list_per_page = 20
    ordering = ('-created_at',)
    exclude = ('created_at', 'updated_at',)

    def save_model(self, request, obj, form, change):
        obj.slug = slugify(obj.title)
        obj.save(using=db_name)

admin.site.register(Saying, SayingAdmin)
