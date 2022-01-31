from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('category','created_on','modefied_on')
    list_per_page = 10


@admin.register(models.Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('category','product_title','price','description','thumbnail_preview','created_on','modefied_on')
    readonly_fields = ('thumbnail_preview',)
    list_filter = ("category","created_on")
    list_per_page = 10
    search_fields = ['product_title','category__category']

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = "Product's Image"
    thumbnail_preview.allow_tags = True