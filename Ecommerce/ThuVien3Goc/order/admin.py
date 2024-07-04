from django.contrib import admin
from .models import Checkout, OrderItems

# Register your models here.
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ['code', 'person_name', 'address', 'phone', 'email', 'total', 'status', 'date_order']
    list_display_links = ['code', 'person_name']
    list_per_page = 20
    ordering = ('-date_order',)
    exclude = ('code', 'updated_at',)

    def save_model(self, request, obj, form, change):
        obj.code = obj.generate_code()
        obj.save()

admin.site.register(Checkout, CheckoutAdmin)

class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ['product_slug', 'price', 'quantity', 'checkout']
    list_display_links = ['product_slug']
    list_per_page = 20
    ordering = ('-created_at',)
    exclude = ('created_at', 'updated_at',)

admin.site.register(OrderItems, OrderItemsAdmin)

