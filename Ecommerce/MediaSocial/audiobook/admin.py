from django.contrib import admin
from .models import AudioBook, BookSection
from django.utils.text import slugify

db_name = "default"

# Register your models here.
class AudioBookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'producer', 'is_active', 'created_at', 'updated_at']
    list_filter = ['author', 'producer', 'is_active']
    search_fields = ['title', 'author', 'producer']
    list_per_page = 10
    ordering = ['-created_at']
    exclude = ['created_at', 'updated_at']
    prepopulated_fields = {'slug': ('title',)}
    
    def save_model(self, request, obj, form, change):
        obj.slug = slugify(obj.title)
        obj.save(using=db_name)
    
admin.site.register(AudioBook, AudioBookAdmin)

class BookSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'audio_book', 'file_type', 'is_active', 'created_at', 'updated_at']
    list_filter = ['audio_book', 'file_type', 'is_active']
    search_fields = ['title', 'audio_book', 'file_type']
    list_per_page = 10
    ordering = ['-created_at']
    exclude = ['created_at', 'updated_at']
    prepopulated_fields = {'slug': ('title',)}
    
    def save_model(self, request, obj, form, change):
        obj.slug = slugify(obj.title)
        obj.save(using=db_name)
    
admin.site.register(BookSection, BookSectionAdmin)
    
