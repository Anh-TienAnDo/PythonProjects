from django.contrib import admin
from .models import *

# Register your models here.
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

class DoctorAdmin(admin.ModelAdmin):
    # Xác định các trường hiển thị trên danh sách các sản phẩm trong trang admin.
    list_display = ('slug', 'name',  'email', 'phone', 'created_at', 'updated_at', )
    # Số lượng sản phẩm được hiển thị trên mỗi trang danh sách
    list_per_page = 20
    # sắp xếp mặc định của danh sách sản phẩm.
    ordering = ['-created_at']
    # Cho phép tìm kiếm các sản phẩm theo các trường được chỉ định.
    search_fields = ['slug', 'name',  'email',]
    # Loại bỏ các trường từ biểu mẫu chỉnh sửa.
    exclude = ('slug', 'created_at', 'updated_at',)

# Register your models here.
admin.site.register(Doctor, DoctorAdmin)

class LevelAdmin(admin.ModelAdmin):
    # Xác định các trường hiển thị trên danh sách các sản phẩm trong trang admin.
    list_display = ('slug', 'name',  'is_active', 'created_at', 'updated_at', )
    # Số lượng sản phẩm được hiển thị trên mỗi trang danh sách
    list_per_page = 20
    # sắp xếp mặc định của danh sách sản phẩm.
    ordering = ['-created_at']
    # Cho phép tìm kiếm các sản phẩm theo các trường được chỉ định.
    search_fields = ['slug', 'name',]
    # Loại bỏ các trường từ biểu mẫu chỉnh sửa.
    exclude = ('slug', 'created_at', 'updated_at',)

# Register your models here.
admin.site.register(Level, LevelAdmin)

class NameAdmin(admin.ModelAdmin):
    # Xác định các trường hiển thị trên danh sách các sản phẩm trong trang admin.
    list_display = ('fname', 'lname',  'fullname', 'created_at', 'updated_at', )
    # Số lượng sản phẩm được hiển thị trên mỗi trang danh sách
    list_per_page = 20
    # sắp xếp mặc định của danh sách sản phẩm.
    ordering = ['-created_at']
    # Cho phép tìm kiếm các sản phẩm theo các trường được chỉ định.
    search_fields = ['fname', 'lname',  'fullname',]
    # Loại bỏ các trường từ biểu mẫu chỉnh sửa.
    exclude = ('fullname', 'created_at', 'updated_at',)

# Register your models here.
admin.site.register(Name, NameAdmin)

class PlaceWorkAdmin(admin.ModelAdmin):
    # Xác định các trường hiển thị trên danh sách các sản phẩm trong trang admin.
    list_display = ('slug', 'name',  'is_active', 'created_at', 'updated_at', )
    # Số lượng sản phẩm được hiển thị trên mỗi trang danh sách
    list_per_page = 20
    # sắp xếp mặc định của danh sách sản phẩm.
    ordering = ['-created_at']
    # Cho phép tìm kiếm các sản phẩm theo các trường được chỉ định.
    search_fields = ['slug', 'name',]
    # Loại bỏ các trường từ biểu mẫu chỉnh sửa.
    exclude = ('slug', 'created_at', 'updated_at',)

# Register your models here.
admin.site.register(PlaceWork, PlaceWorkAdmin)

class SpecialtyAdmin(admin.ModelAdmin):
    # Xác định các trường hiển thị trên danh sách các sản phẩm trong trang admin.
    list_display = ('slug', 'name',  'is_active', 'created_at', 'updated_at', )
    # Số lượng sản phẩm được hiển thị trên mỗi trang danh sách
    list_per_page = 20
    # sắp xếp mặc định của danh sách sản phẩm.
    ordering = ['-created_at']
    # Cho phép tìm kiếm các sản phẩm theo các trường được chỉ định.
    search_fields = ['slug', 'name',]
    # Loại bỏ các trường từ biểu mẫu chỉnh sửa.
    exclude = ('slug', 'created_at', 'updated_at',)

# Register your models here.
admin.site.register(Specialty, SpecialtyAdmin)