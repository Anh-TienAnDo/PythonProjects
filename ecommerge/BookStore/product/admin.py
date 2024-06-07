from django.contrib import admin
from .models import *
from .forms import ProductAdminForm
from unidecode import unidecode
from django.utils.text import slugify

class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
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
        obj.slug = slugify(unidecode(obj.name))
        obj.save(using='mongodb')
    # Trả về queryset mặc định cho trang admin.
    # chỉ định dữ liệu sẽ được lấy từ cơ sở dữ liệu 'mongodb'.
    def get_queryset(self, request):
        return Product.objects.using('mongodb')

# Register your models here.
admin.site.register(Product, ProductAdmin)
