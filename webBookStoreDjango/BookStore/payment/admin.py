from django.contrib import admin
from .models import *

# Register your models here.
db_name = "payment"

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('code', 'bank', 'checkout', 'total', 'paymented', 'missing', 'completed', 'date_completed',)
    list_display_links = ('code', 'bank', 'checkout',)
    # Số lượng sản phẩm được hiển thị trên mỗi trang danh sách
    list_per_page = 20
    # sắp xếp mặc định của danh sách sản phẩm.
    ordering = ['-updated_at']
    # Cho phép tìm kiếm các sản phẩm theo các trường được chỉ định.
    search_fields = ['code', 'bank', 'checkout',]
    # Loại bỏ các trường từ biểu mẫu chỉnh sửa.
    exclude = ('create_at', 'updated_at',)
    # chỉ định cơ sở dữ liệu được sử dụng là 'mongodb'.
    def save_model(self, request, obj, form, change):
        obj.save(using=db_name)
    def get_queryset(self, request):
        return Payment.objects.using(db_name)

admin.site.register(Payment, PaymentAdmin)