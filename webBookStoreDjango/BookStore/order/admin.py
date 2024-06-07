from django.contrib import admin
from .models import OrderItems, Checkout

# Register your models here.
db_name = "order"
class CheckoutAdmin(admin.ModelAdmin):
    # Xác định các trường hiển thị trên danh sách các sản phẩm trong trang admin.
    list_display = ('user_id', 'code', 'name', 'phone', 'email', 'status', 'date_order', 'updated_at',)
    # Chỉ định các trường liên kết từ danh sách đến trang chỉnh sửa chi tiết.
    list_display_links = ('user_id', 'code', 'name',)
    # Số lượng sản phẩm được hiển thị trên mỗi trang danh sách
    list_per_page = 20
    # sắp xếp mặc định của danh sách sản phẩm.
    ordering = ['-date_order']
    # Cho phép tìm kiếm các sản phẩm theo các trường được chỉ định.
    search_fields = ['user_id', 'code', 'name', 'phone', 'email', 'status',]
    # Loại bỏ các trường từ biểu mẫu chỉnh sửa.
    exclude = ('date_order', 'updated_at',)
    # Phương thức này được gọi khi một đối tượng được lưu.
    # chỉ định cơ sở dữ liệu được sử dụng là 'mongodb'.
    def save_model(self, request, obj, form, change):
        # obj.code = _generate_code
        obj.save(using=db_name)
    def get_queryset(self, request):
        return Checkout.objects.using(db_name)

class OrderItemsAdmin(admin.ModelAdmin):
    # Xác định các trường hiển thị trên danh sách các sản phẩm trong trang admin.
    list_display = ('product_slug', 'price', 'quantity',)
    # Chỉ định các trường liên kết từ danh sách đến trang chỉnh sửa chi tiết.
    list_display_links = ('product_slug',)
    # Số lượng sản phẩm được hiển thị trên mỗi trang danh sách
    list_per_page = 20
    # sắp xếp mặc định của danh sách sản phẩm.
    ordering = ['-price']
    # Cho phép tìm kiếm các sản phẩm theo các trường được chỉ định.
    search_fields = ['product_slug', 'price',]
    # Loại bỏ các trường từ biểu mẫu chỉnh sửa.
    exclude = ()
    # Phương thức này được gọi khi một đối tượng được lưu.
    # chỉ định cơ sở dữ liệu được sử dụng là 'mongodb'.
    def save_model(self, request, obj, form, change):
        obj.save(using=db_name)
    def get_queryset(self, request):
        return OrderItems.objects.using(db_name)

admin.site.register(OrderItems, OrderItemsAdmin)
admin.site.register(Checkout, CheckoutAdmin)
