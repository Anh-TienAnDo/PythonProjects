from django.contrib import admin
from .models import Cart
from .cart import _generate_cart_id

# Register your models here.
db_name = "default"
class CartAdmin(admin.ModelAdmin):
    # form = MobileAdminForm
    # Xác định các trường hiển thị trên danh sách các sản phẩm trong trang admin.
    list_display = ('cart_id', 'user_id', 'product_slug', 'quantity', 'created_at', 'updated_at',)
    # Chỉ định các trường liên kết từ danh sách đến trang chỉnh sửa chi tiết.
    list_display_links = ('cart_id', 'user_id', 'product_slug',)
    # Số lượng sản phẩm được hiển thị trên mỗi trang danh sách
    list_per_page = 20
    # sắp xếp mặc định của danh sách sản phẩm.
    ordering = ['-created_at']
    # Cho phép tìm kiếm các sản phẩm theo các trường được chỉ định.
    search_fields = ['cart_id', 'user_id', 'product_slug',]
    # Loại bỏ các trường từ biểu mẫu chỉnh sửa.
    exclude = ('cart_id', 'created_at', 'updated_at',)
    # Phương thức này được gọi khi một đối tượng được lưu.
    # chỉ định cơ sở dữ liệu được sử dụng là 'mongodb'.
    def save_model(self, request, obj, form, change):
        obj.cart_id = _generate_cart_id()
        obj.save(using=db_name)
    def get_queryset(self, request):
        return Cart.objects.using(db_name)

admin.site.register(Cart, CartAdmin)
