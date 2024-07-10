from django.contrib import admin
from .models import Type
from django.utils.text import slugify
db_name = "default"

# Register your models here.
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at', 'updated_at']
    list_display_links = ('name',)
    list_per_page = 20
    search_fields = ['name', 'slug']
    exclude = ('created_at', 'updated_at',)
    list_filter = ['is_active', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['-created_at']

    def save_model(self, request, obj, form, change):
        obj.slug = slugify(obj.name)
        obj.save(using=db_name)

admin.site.register(Type, TypeAdmin)

