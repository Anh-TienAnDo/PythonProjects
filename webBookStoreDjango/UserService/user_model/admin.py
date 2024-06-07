from django.contrib import admin
from .models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    # form = MobileAdminForm
    # Xác định các trường hiển thị trên danh sách các sản phẩm trong trang admin.
    list_display = ('account', 'address', 'name_user', 'phone', 'created_at', 'updated_at', )
    # Chỉ định các trường liên kết từ danh sách đến trang chỉnh sửa chi tiết.
    list_display_links = ('account', 'address', 'name_user',)
    # Số lượng sản phẩm được hiển thị trên mỗi trang danh sách
    list_per_page = 20
    # sắp xếp mặc định của danh sách sản phẩm.
    ordering = ['-created_at']
    # Cho phép tìm kiếm các sản phẩm theo các trường được chỉ định.
    search_fields = ['phone',]
    # Loại bỏ các trường từ biểu mẫu chỉnh sửa.
    exclude = ('created_at', 'updated_at',)

# Register your models here.
admin.site.register(User, UserAdmin)

class AccountAdmin(admin.ModelAdmin):
    # Xác định các trường hiển thị trên danh sách các sản phẩm trong trang admin.
    list_display = ('username', 'password', 'email', 'is_active', 'is_staff', 'date_joined', )
    # Chỉ định các trường liên kết từ danh sách đến trang chỉnh sửa chi tiết.
    list_display_links = ('username',)
    # Số lượng sản phẩm được hiển thị trên mỗi trang danh sách
    list_per_page = 20
    # sắp xếp mặc định của danh sách sản phẩm.
    ordering = ['-date_joined']
    # Cho phép tìm kiếm các sản phẩm theo các trường được chỉ định.
    search_fields = ['username', 'email', 'is_staff']
    # Loại bỏ các trường từ biểu mẫu chỉnh sửa.
    exclude = ('date_joined',)

# Register your models here.
admin.site.register(Account, AccountAdmin)

class NameUserAdmin(admin.ModelAdmin):
    # Xác định các trường hiển thị trên danh sách các sản phẩm trong trang admin.
    list_display = ('fullname', 'fname', 'lname',  'created_at', 'updated_at', )
    # Chỉ định các trường liên kết từ danh sách đến trang chỉnh sửa chi tiết.
    list_display_links = ('fullname',)
    # Số lượng sản phẩm được hiển thị trên mỗi trang danh sách
    list_per_page = 20
    # sắp xếp mặc định của danh sách sản phẩm.
    ordering = ['-created_at']
    # Cho phép tìm kiếm các sản phẩm theo các trường được chỉ định.
    search_fields = ['fullname', 'fname', 'lname',]
    # Loại bỏ các trường từ biểu mẫu chỉnh sửa.
    exclude = ('fullname', 'created_at', 'updated_at',)
    # Phương thức này được gọi khi một đối tượng được lưu.
    # chỉ định cơ sở dữ liệu được sử dụng là 'mongodb'.
    def save_model(self, request, obj, form, change):
        obj.fullname = str(obj.lname) + " " +str(obj.fname)
        obj.save(using='default')

# Register your models here.
admin.site.register(NameUser, NameUserAdmin)

class AddressAdmin(admin.ModelAdmin):
    # Xác định các trường hiển thị trên danh sách các sản phẩm trong trang admin.
    list_display = ('street', 'district',  'city', 'created_at', 'updated_at', )
    # Số lượng sản phẩm được hiển thị trên mỗi trang danh sách
    list_per_page = 20
    # sắp xếp mặc định của danh sách sản phẩm.
    ordering = ['-created_at']
    # Cho phép tìm kiếm các sản phẩm theo các trường được chỉ định.
    search_fields = ['street', 'district', 'city',]
    # Loại bỏ các trường từ biểu mẫu chỉnh sửa.
    exclude = ('created_at', 'updated_at',)

# Register your models here.
admin.site.register(Address, AddressAdmin)
