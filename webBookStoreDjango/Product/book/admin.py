from django.contrib import admin
from .models import *

# Register your models here.
from django.utils.text import slugify
db_name = "book"

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    # form = MobileAdminForm
    # Xác định các trường hiển thị trên danh sách các sản phẩm trong trang admin.
    list_display = ('name', 'price', 'old_price', 'created_at', 'updated_at',)
    # Chỉ định các trường liên kết từ danh sách đến trang chỉnh sửa chi tiết.
    list_display_links = ('name',)
    # Số lượng sản phẩm được hiển thị trên mỗi trang danh sách
    list_per_page = 20
    # sắp xếp mặc định của danh sách sản phẩm.
    ordering = ['-created_at']
    # Cho phép tìm kiếm các sản phẩm theo các trường được chỉ định.
    search_fields = ['name', 'description',]
    # Loại bỏ các trường từ biểu mẫu chỉnh sửa.
    exclude = ('created_at', 'updated_at',)
    # Thiết lập trường slug để tự động được điền dựa trên trường name.
    prepopulated_fields = {'slug': ('name',)}
    # Phương thức này được gọi khi một đối tượng được lưu.
    # chỉ định cơ sở dữ liệu được sử dụng là 'mongodb'.
    def save_model(self, request, obj, form, change):
        obj.slug = slugify(obj.name)
        # obj.save(using='mongodb')
        obj.save(using=db_name)
    def get_queryset(self, request):
        # return Phone.objects.using('mongodb')
        return Book.objects.using(db_name)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['-created_at']
    search_fields = ['name',]
    exclude = ('created_at', 'updated_at',)
    # Phương thức này được gọi khi một đối tượng được lưu.
    prepopulated_fields = {'slug': ('name',)}
    def save_model(self, request, obj, form, change):
        obj.slug = slugify(obj.name)
        obj.save(using=db_name)
    def get_queryset(self, request):
        # return Type.objects.using('mongodb')
        return Category.objects.using(db_name)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['-created_at']
    search_fields = ['name',]
    exclude = ('created_at', 'updated_at',)
    def save_model(self, request, obj, form, change):
        obj.save(using=db_name)
    def get_queryset(self, request):
        # return Type.objects.using('mongodb')
        return Author.objects.using(db_name)

class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['-created_at']
    search_fields = ['name',]
    exclude = ('created_at', 'updated_at',)
    def save_model(self, request, obj, form, change):
        obj.save(using=db_name)
    def get_queryset(self, request):
        # return Type.objects.using('mongodb')
        return Publisher.objects.using(db_name)

# Register your models here.
# admin.site.register(Phone, PhoneAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Publisher, PublisherAdmin)

