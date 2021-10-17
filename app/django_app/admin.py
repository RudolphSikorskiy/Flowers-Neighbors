from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Customer, Manager, Store, Product, ProductInStore, Order


# Register your models here.


@admin.register(Customer)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "username", "email", "phone", 'created_at', 'updated_at')
    search_fields = ("full_name", "username", "email", "phone")


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "username", "email", "phone", 'created_at', 'updated_at')


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "city", "street", "house", "phone_number", "email", 'created_at', 'updated_at')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", 'created_at', 'updated_at', "get_image")
    list_editable = ("price",)
    list_per_page = 8
    list_max_show_all = 10
    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.photo.url}" width=80px')


#
#
#
@admin.register(ProductInStore)
class ProductInStoreAdmin(admin.ModelAdmin):
    list_display = ("id", "store", "product", 'created_at', 'updated_at')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'successful', 'created_at', 'updated_at', "id", "customer_id", "product_id")
    list_display_links = ("id", "customer_id", "customer_id", "customer_id")
    list_filter = ('successful',)
    list_editable = ('successful',)
    list_per_page = 20
    list_max_show_all = 100
