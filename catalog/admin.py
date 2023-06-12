from django.contrib import admin

from catalog.models import Product, Category, Blog, Version


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'data', 'preview', 'date_create', 'views_count', 'is_active')
    list_filter = ('date_create',)
    search_fields = ('title',)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('title_version', 'product',)
    list_filter = ('product',)
