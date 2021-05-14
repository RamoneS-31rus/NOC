from django.contrib import admin
from .models import Address, Contact


class AdminAddress(admin.ModelAdmin):
    model = Address
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Address)
admin.site.register(Contact)
