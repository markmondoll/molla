from django.contrib import admin
from store.models import Category, Product, ProductImages


class ProductImagesAdmin(admin.StackedInline):
    model = ProductImages

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    prepopulated_fields = {"slug": ('title',)}
    

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)