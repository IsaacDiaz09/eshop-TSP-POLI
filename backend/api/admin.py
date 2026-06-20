from django.contrib import admin
from .models import Category, Product, ProductVariant, Order, OrderItem

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 4

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brand', 'category', 'price')
    list_filter = ('category', 'brand')
    search_fields = ('name', 'brand', 'description')
    inlines = [ProductVariantInline]

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'size', 'color', 'stock')
    list_filter = ('size', 'color', 'product__brand')
    search_fields = ('product__name', 'color')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'variant', 'quantity', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'id')
    inlines = [OrderItemInline]
    readonly_fields = ('user', 'total_price', 'created_at')
