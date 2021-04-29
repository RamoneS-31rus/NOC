from django.contrib import admin
from .models import Category, Type, Product, Income


class AdminProduct(admin.ModelAdmin):
    model = Product
    prepopulated_fields = {'slug': ('name',)}


# class AdminIncome(admin.ModelAdmin):
#     model = Income
#     prepopulated_fields = {'income_slug': ('income_name',)}


admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Product, AdminProduct)
admin.site.register(Income)
