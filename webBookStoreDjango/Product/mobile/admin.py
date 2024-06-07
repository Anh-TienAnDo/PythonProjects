from django.contrib import admin
from .models import *

# Register your models here.
from django.utils.text import slugify
db_name = "mobile"

# Register your models here.
class MobileAdmin(admin.ModelAdmin):
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
        return Phone.objects.using(db_name)


class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['-created_at']
    search_fields = ['name',]
    exclude = ('created_at', 'updated_at',)
    prepopulated_fields = {'slug': ('name',)}
    def save_model(self, request, obj, form, change):
        obj.slug = slugify(obj.name)
        obj.save(using=db_name)
    def get_queryset(self, request):
        # return Type.objects.using('mongodb')
        return Type.objects.using(db_name)

class ProducerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['-created_at']
    search_fields = ['name',]
    exclude = ('created_at', 'updated_at',)
    prepopulated_fields = {'slug': ('name',)}
    # Phương thức này được gọi khi một đối tượng được lưu.
    # chỉ định cơ sở dữ liệu được sử dụng là 'mongodb'.
    def save_model(self, request, obj, form, change):
        obj.slug = slugify(obj.name)
        obj.save(using=db_name)
    def get_queryset(self, request):
        # return Producer.objects.using('mongodb')
        return Producer.objects.using(db_name)

# Register your models here.
# admin.site.register(Phone, PhoneAdmin)
admin.site.register(Phone, MobileAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Producer, ProducerAdmin )

