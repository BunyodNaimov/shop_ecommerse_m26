from django.contrib import admin

from shop.models.categories import Category
from shop.models.orders import Basket, Order
from shop.models.products import Product, ProductImage, ProductAttribute, ProductVariation, ProductColor


# Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


#  Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'quantity')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(ProductImage)
admin.site.register(ProductAttribute)
admin.site.register(ProductVariation)
admin.site.register(ProductColor)
admin.site.register(Basket)
admin.site.register(Order)
