from django.contrib import admin
from .models import User, Category, Product, ProductImage

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('is_active', 'is_staff')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_styled_name', 'name_ru', 'parent', 'is_active')
    search_fields = ('name_uz', 'name_ru')
    list_filter = ('parent', 'is_active')

    def get_styled_name(self, obj):
        """Ichki kategoriyalarni vizual jihatdan ajratib ko'rsatish funksiyasi"""
        if obj.parent:
            return f"↳ {obj.name_uz}"  
        return obj.name_uz  
    
    get_styled_name.short_description = 'Name uz'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uz', 'name_ru', 'price', 'category', 'is_active')
    search_fields = ('name_uz', 'name_ru')
    list_filter = ('is_active', 'category')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'created_at')
    search_fields = ('product__name_uz', 'product__name_ru')
    list_filter = ('created_at',)