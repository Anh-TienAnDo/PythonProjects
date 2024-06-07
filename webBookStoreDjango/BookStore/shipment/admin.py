from django.contrib import admin
from .models import *

# Register your models here.
db_name = "shipment"

# Register your models here.
class ShipmentAdmin(admin.ModelAdmin):
    # form = MobileAdminForm
    # Xác định các trường hiển thị trên danh sách các sản phẩm trong trang admin.
    list_display = ('checkout', 'code', 'shipper', 'delivered', 'date_shipment',)
    # Chỉ định các trường liên kết từ danh sách đến trang chỉnh sửa chi tiết.
    list_display_links = ('checkout', 'code',)
    # Số lượng sản phẩm được hiển thị trên mỗi trang danh sách
    list_per_page = 20
    # sắp xếp mặc định của danh sách sản phẩm.
    ordering = ['-date_shipment']
    # Cho phép tìm kiếm các sản phẩm theo các trường được chỉ định.
    search_fields = ['code', 'shipper', 'delivered', 'date_shipment',]
    # Loại bỏ các trường từ biểu mẫu chỉnh sửa.
    exclude = ('code', 'date_shipment',)
    # Phương thức này được gọi khi một đối tượng được lưu.
    # chỉ định cơ sở dữ liệu được sử dụng là 'mongodb'.
    def save_model(self, request, obj, form, change):
        obj.save(using=db_name)
    def get_queryset(self, request):
        # return Phone.objects.using('mongodb')
        return Shipment.objects.using(db_name)

# Register your models here.
admin.site.register(Shipment, ShipmentAdmin)

