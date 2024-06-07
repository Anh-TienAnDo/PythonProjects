from django.contrib import admin
from .models import Category
from unidecode import unidecode
from django.utils.text import slugify

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at', )
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    search_fields = ['name', 'description',]
    exclude = ('created_at', 'updated_at',)

    prepopulated_fields = {'slug':('name',)}

    def save_model(self, request, obj, form, change):
        obj.slug = slugify(unidecode(obj.name))
        obj.save(using='mongodb')

    def get_queryset(self, request):
        return Category.objects.using('mongodb')

# Register your models here.
admin.site.register(Category, CategoryAdmin)
