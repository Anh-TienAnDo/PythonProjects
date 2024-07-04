from django.contrib import admin
from .models import CartItems

db_name = "default"
# Register your models here.
class CartItemsAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_slug', 'quantity', 'price', 'user_id', 'created_at']
    list_display_links = ['product_slug']
    list_per_page = 20
    ordering = ('-created_at',)
    exclude = ('id', 'created_at', 'updated_at',)

    def save_model(self, request, obj, form, change):
        obj.id = obj.generate_cart_id()
        obj.save(using=db_name)

admin.site.register(CartItems, CartItemsAdmin)

